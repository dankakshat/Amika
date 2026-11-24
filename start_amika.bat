@echo off
title OpenAmika Lite (Potato Laptop Edition)
echo ========================================================
echo        OpenAmika Lite - Starting Server...
echo ========================================================
echo.
cd /d "%~dp0"
echo Starting FastAPI Web Server at http://localhost:8000
start http://localhost:8000
python app.py
pause
