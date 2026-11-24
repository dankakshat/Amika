@echo off
title OpenAmika - Remove Autostart
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set SHORTCUT=%STARTUP_FOLDER%\OpenAmika.lnk

if exist "%SHORTCUT%" (
    del "%SHORTCUT%"
    echo ========================================================
    echo   [SUCCESS] OpenAmika Lite removed from Windows Startup.
    echo ========================================================
) else (
    echo OpenAmika shortcut was not found in Startup.
)
echo.
pause
