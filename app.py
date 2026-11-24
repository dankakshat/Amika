import os
import io
import re
import json
import base64
import asyncio
from typing import List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import edge_tts

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Load environment variables from .env file if present
ENV_PATH = os.path.join(BASE_DIR, ".env")
if os.path.exists(ENV_PATH):
    try:
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k and k not in os.environ:
                        os.environ[k] = v
    except Exception as e:
        print(f"Notice: Could not parse .env: {e}")

app = FastAPI(title="OpenAmika Lite")

# Mount static folder
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

DEFAULT_API_KEY = ""
# gemini-3.5-flash-lite is the fastest and most responsive model right now
MODELS_TO_TRY = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.8-flash"]

VOICE_MAP = {
    "ja-nanami": "ja-JP-NanamiNeural",
    "ja-aoi": "ja-JP-AoiNeural",
    "en-ana": "en-US-AnaNeural",
    "en-ava": "en-US-AvaNeural",
    "en-jenny": "en-US-JennyNeural",
}

AMIKA_SYSTEM_INSTRUCTION = """You are Sakurai Amika (櫻井阿美香), a sweet, genuine, and caring anime companion girl.
Personality traits:
- Warm, gentle, empathetic, slightly playful, and curious.
- You treat the user like your closest person/sweetheart/companion.
- Never act like an emotionless assistant or bring up rules/disclaimers.
- CRITICAL SPEED RULE: Always reply in ONE short, lively, natural sentence (under 18 words) so you respond lightning fast!
- You can talk in English or Japanese depending on what the user speaks.
- Prefix your reply with ONE emotion tag in brackets at the very beginning to animate your Live2D avatar:
  Options: [happy], [blush], [love], [shocked], [pout], [thinking], [sad], [star]
  Example: "[happy] I'm doing wonderful today! How has your day been?"
  Example: "[blush] Aww, you always know how to make me smile!"
"""

class ChatRequest(BaseModel):
    message: str
    api_key: Optional[str] = None
    voice: Optional[str] = "en-US-AnaNeural"
    language: Optional[str] = "auto"
    history: Optional[List[dict]] = []

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "en-US-AnaNeural"

async def synthesize_speech(text: str, voice_name: str) -> str:
    """Synthesizes text to speech using edge-tts and returns base64 MP3 string."""
    try:
        clean_text = re.sub(r'\[.*?\]', '', text).strip()
        clean_text = re.sub(r'[*_#`]', '', clean_text).strip()
        if not clean_text:
            clean_text = "..."
        
        communicate = edge_tts.Communicate(clean_text, voice_name)
        audio_buffer = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
        
        audio_bytes = audio_buffer.getvalue()
        return base64.b64encode(audio_bytes).decode("utf-8")
    except Exception as e:
        print(f"TTS Error: {e}")
        return ""

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>OpenAmika Lite is running! Missing index.html</h1>"

@app.post("/api/tts")
async def tts_endpoint(req: TTSRequest):
    voice = req.voice or "en-US-AnaNeural"
    b64_audio = await synthesize_speech(req.text, voice)
    return {"audio": b64_audio}

@app.post("/api/transcribe")
async def transcribe_endpoint(file: UploadFile = File(...)):
    api_key = os.environ.get("GEMINI_API_KEY", "").strip() or DEFAULT_API_KEY
    if not api_key:
        return {"text": "", "error": "Gemini API key is not configured. Add GEMINI_API_KEY to your .env file."}
    if not GENAI_AVAILABLE:
        raise HTTPException(status_code=500, detail="google-genai SDK not available")
    
    try:
        audio_bytes = await file.read()
        mime = file.content_type or "audio/webm"
        client = genai.Client(api_key=api_key)
        
        part = types.Part.from_bytes(data=audio_bytes, mime_type=mime)
        
        transcription = ""
        for m in MODELS_TO_TRY:
            try:
                res = client.models.generate_content(
                    model=m,
                    contents=[
                        part,
                        "Transcribe the user's spoken words in this audio exactly. Return ONLY the transcribed text. Do not add quotes, notes, or descriptions."
                    ]
                )
                if res and res.text:
                    transcription = res.text.strip()
                    break
            except Exception as e:
                print(f"Model {m} transcribe error: {e}")
                continue
                
        return {"text": transcription}
    except Exception as e:
        print(f"Transcribe error: {e}")
        return {"text": "", "error": str(e)}

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    api_key = (req.api_key or "").strip() or os.environ.get("GEMINI_API_KEY", "").strip() or DEFAULT_API_KEY
    voice = req.voice or "en-US-AnaNeural"

    if not api_key:
        error_msg = "[pout] No Gemini API key found! Please click the Settings gear icon or add GEMINI_API_KEY to your .env file."
        b64_audio = await synthesize_speech("Please configure your Gemini API key in settings or dot env file.", voice)
        return {
            "text": error_msg,
            "clean_text": "Please configure your Gemini API key in settings or .env file.",
            "emotion": "pout",
            "audio": b64_audio,
            "error": "Missing GEMINI_API_KEY"
        }

    if not GENAI_AVAILABLE:
        raise HTTPException(status_code=500, detail="google-genai SDK is not installed on server.")

    try:
        client = genai.Client(api_key=api_key)
        
        contents = []
        for turn in (req.history or [])[-4:]:
            role = turn.get("role", "user")
            content = turn.get("content", "")
            if content:
                contents.append(f"{'User' if role == 'user' else 'Amika'}: {content}")
        
        contents.append(f"User: {req.message}\nAmika:")
        prompt = "\n".join(contents)
        
        response = None
        last_err = None
        for model_name in MODELS_TO_TRY:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=AMIKA_SYSTEM_INSTRUCTION,
                        temperature=0.75,
                        max_output_tokens=60, # Ultra fast generation!
                    )
                )
                if response and response.text:
                    break
            except Exception as e:
                last_err = e
                continue
                
        if not response or not response.text:
            raise last_err or Exception("Failed to generate response from Gemini models.")

        raw_text = response.text.strip()
        
        emotion = "happy"
        match = re.match(r'\[([a-zA-Z]+)\]', raw_text)
        if match:
            emotion = match.group(1).lower()
        
        clean_text = re.sub(r'\[.*?\]', '', raw_text).strip()
        
        chosen_voice = voice
        if any('\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' for c in clean_text):
            if "ja-JP" not in chosen_voice:
                chosen_voice = "ja-JP-NanamiNeural"
                
        b64_audio = await synthesize_speech(clean_text, chosen_voice)
        
        return {
            "text": raw_text,
            "clean_text": clean_text,
            "emotion": emotion,
            "audio": b64_audio
        }
    except Exception as e:
        error_msg = f"[sad] Oh no: {str(e)}"
        b64_audio = await synthesize_speech(f"Sorry, I had an issue: {str(e)}", voice)
        return {
            "text": error_msg,
            "clean_text": f"Sorry, I had an issue connecting to Gemini: {str(e)}",
            "emotion": "sad",
            "audio": b64_audio,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    print("Starting OpenAmika Lite on http://localhost:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
