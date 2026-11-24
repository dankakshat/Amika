# 🌸 OpenAmika Lite (Potato Laptop Edition)

> A lightweight, ultra-responsive AI VTuber companion designed to run smoothly on any low-spec laptop without needing an NVIDIA GPU or 40 GB of local models.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688.svg)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-Flash--Lite-orange.svg)](https://aistudio.google.com/)
[![Live2D](https://img.shields.io/badge/Live2D-Cubism%204-ff69b4.svg)](https://www.live2d.com/)

---

## ✨ Features

- **🚀 Ultra Lightweight:** Zero heavy local neural models or CUDA GPU requirements. Runs effortlessly on everyday laptops.
- **⚡ Lightning-Fast Brain:** Powered by Google's `gemini-3.5-flash-lite` for conversational replies in ~1 second.
- **🎨 Live2D Interactive Avatar:** Full Cubism 4 rendering with smooth idle breathing, eye blinking, hair physics, and cursor tracking.
- **🗣️ Real-time Lip Sync:** Web Audio API frequency analysis accurately drives Amika's mouth (`ParamMouthOpenY`) in real time as she speaks.
- **🎭 Expressive Emotions:** Dynamic Live2D facial expressions automatically trigger based on mood tags (`[happy]`, `[blush]`, `[love]`, `[shocked]`, `[pout]`, `[thinking]`, `[sad]`, `[star]`).
- **📞 Hands-Free Realtime Voice Call:** Continuous conversation powered by browser Voice Activity Detection (VAD). Speak freely and Amika automatically answers when you finish your sentence — no buttons needed!
- **⚡ Fast Multimodal Voice Chat:** Single-hop `/api/voice_chat` combining Gemini audio understanding and Edge-TTS synthesis for instant sub-2s conversational turnaround.
- **🔊 Natural Neural Voice:** Crystal-clear speech synthesis using Microsoft Edge TTS (English and Japanese voices).
- **🖱️ Interactive Camera Controls:** Click and drag to pan the model, mouse wheel to zoom in/out, and a quick Reset View button.
- **🖥️ Desktop & 24/7 Autostart:** Windows batch scripts and VBS launchers for background startup or 24/7 companion mode.

---

## 📋 Prerequisites

- Python 3.10 or higher
- A free Google Gemini API Key ([Get one here from Google AI Studio](https://aistudio.google.com/))
- Any modern web browser (Floorp, Chrome, Edge, Brave, Firefox)

---

## 🛠️ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/dankakshat/Amika.git
cd Amika
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure your API Key
Copy `.env.example` to `.env` and insert your Gemini API Key:
```bash
cp .env.example .env
```
In `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Alternatively, you can leave it blank and paste your key in the **Settings** menu directly inside the app!)*

### 4. Run Amika!
Double-click `start_amika.bat` or run:
```bash
python app.py
```
Open your browser at:
```
http://localhost:8000
```

---

## ⚙️ Project Structure

```
├── app.py                      # FastAPI backend (Gemini brain + Edge-TTS + Audio Transcribe)
├── requirements.txt            # Python dependencies
├── .env.example                # Template for Gemini API key
├── start_amika.bat             # Quick launcher for local web server
├── Launch_Amika_App.bat        # App window launcher
├── Amika_Desktop_App.vbs       # Silent background launcher
├── install_autostart_24_7.bat  # Adds Amika to Windows Startup (starts on boot)
├── uninstall_autostart.bat    # Removes Amika from Windows Startup
└── static/
    ├── index.html              # Frontend with Pixi.js, Live2D Cubism 4, and Web Audio
    ├── manifest.json           # PWA manifest
    ├── icon.png                # App icon
    ├── vendor/                 # Pixi.js & Live2D Cubism Core runtime libraries
    └── models/Amika/           # Live2D Cubism model assets & motions
```

---

## 💡 Controls & Tips

- **Realtime Voice Call (Hands-Free):** Click the **"📞 Realtime Call"** button in the top bar. You can speak naturally without clicking anything; Amika detects your speech, waits for your pause, and responds immediately with Live2D lip sync!
- **Push-to-Talk Mic:** Click the microphone button in the chat dock to record a voice message. Amika will transcribe and answer in one fast step.
- **Poke Amika:** Click the "Poke Amika" button or click her head to trigger fun reactions and blushing animations.
- **Adjusting the View:** Left-click and drag anywhere on screen to reposition her; scroll the mouse wheel to zoom. Click "Reset View" to center.
- **Voice Selection:** Switch between Nanami, Aoi, Ana, Ava, and Jenny neural voices in the Settings dialog.

---

## 📜 Credits & Acknowledgments

- **Original Project:** Inspired by [OpenAmika by zeekk0](https://github.com/zeekk0/OpenAmika).
- **Live2D Model:** Amika Live2D model created by [MekaHime](https://huggingface.co/MekaHime/MekaHime_Amika).
- **Live2D Cubism:** Live2D Inc. (Cubism SDK for Web).
- **TTS:** Powered by [edge-tts](https://github.com/rany2/edge-tts).
- **AI Brain:** [Google Gemini API](https://ai.google.dev/).

---

## 📄 License

This repository is shared for educational and personal use.
Live2D Cubism components and the Amika model assets remain subject to their respective creators' licenses.
