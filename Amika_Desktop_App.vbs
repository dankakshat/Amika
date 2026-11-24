Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)

' 1. Start Python backend server silently if not already running
WshShell.CurrentDirectory = currentDir
WshShell.Run "pythonw.exe app.py", 0, False

WScript.Sleep 600

' 2. Launch in Floorp
floorpPath = "C:\Program Files\Ablaze Floorp\floorp.exe"

If fso.FileExists(floorpPath) Then
    WshShell.Run """" & floorpPath & """ -new-window http://127.0.0.1:8000", 1, False
Else
    WshShell.Run "http://127.0.0.1:8000", 1, False
End If
