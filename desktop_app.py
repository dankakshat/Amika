import os
import sys
import time
import threading
import urllib.request
import webview
import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from app import app

SERVER_PORT = 8000
SERVER_URL = f"http://127.0.0.1:{SERVER_PORT}"

def is_server_running():
    try:
        res = urllib.request.urlopen(f"{SERVER_URL}/", timeout=1)
        return res.status == 200
    except Exception:
        return False

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=SERVER_PORT, log_level="warning")

def main():
    # If server is not running, start it in a background thread
    if not is_server_running():
        t = threading.Thread(target=run_server, daemon=True)
        t.start()
        # Wait until server answers
        for _ in range(20):
            if is_server_running():
                break
            time.sleep(0.2)

    # Open PyWebView native desktop window
    window = webview.create_window(
        title="🌸 OpenAmika Lite",
        url=SERVER_URL,
        width=500,
        height=820,
        min_size=(360, 520),
        resizable=True,
        text_select=True,
        background_color="#0d0a14"
    )

    webview.start()

if __name__ == "__main__":
    main()
