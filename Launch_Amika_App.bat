@echo off
title OpenAmika Lite
cd /d "%~dp0"

echo Starting OpenAmika backend...
start "" /b pythonw.exe app.py
timeout /t 1 /nobreak >nul

set FLOORP="C:\Program Files\Ablaze Floorp\floorp.exe"

if exist %FLOORP% (
    start "" %FLOORP% -new-window "http://127.0.0.1:8000"
) else (
    start http://127.0.0.1:8000
)
