@echo off
title OpenAmika - Install 24/7 Autostart
set SCRIPT_DIR=%~dp0
set TARGET_VBS=%SCRIPT_DIR%Amika_Desktop_App.vbs
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set SHORTCUT=%STARTUP_FOLDER%\OpenAmika.lnk

powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT%'); $s.TargetPath='wscript.exe'; $s.Arguments='\"%TARGET_VBS%\"'; $s.WorkingDirectory='%SCRIPT_DIR%'; $s.Save()"

echo ========================================================
echo   [SUCCESS] OpenAmika Lite added to Windows Startup!
echo.
echo   She will now automatically start 24/7 whenever
echo   your laptop boots up or logs in!
echo ========================================================
echo.
pause
