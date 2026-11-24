@echo off
title Create Desktop Shortcut for OpenAmika
set SCRIPT_DIR=%~dp0
set TARGET_VBS=%SCRIPT_DIR%Amika_Desktop_App.vbs

powershell -Command "$desktop=[Environment]::GetFolderPath('Desktop'); $s=(New-Object -COM WScript.Shell).CreateShortcut(\"$desktop\OpenAmika.lnk\"); $s.TargetPath='wscript.exe'; $s.Arguments='\"%TARGET_VBS%\"'; $s.WorkingDirectory='%SCRIPT_DIR%'; $s.Description='OpenAmika AI Companion'; $s.Save()"

echo ========================================================
echo   [SUCCESS] OpenAmika shortcut created on your Desktop!
echo ========================================================
echo.
pause
