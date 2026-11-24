import os
import win32com.client

app_dir = os.path.dirname(os.path.abspath(__file__))
vbs_path = os.path.join(app_dir, "Amika_Desktop_App.vbs")

desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
desktop_lnk = os.path.join(desktop, "OpenAmika.lnk")

startup = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
startup_lnk = os.path.join(startup, "OpenAmika.lnk")

shell = win32com.client.Dispatch("WScript.Shell")

# 1. Desktop shortcut
shortcut = shell.CreateShortCut(desktop_lnk)
shortcut.Targetpath = "wscript.exe"
shortcut.Arguments = f'"{vbs_path}"'
shortcut.WorkingDirectory = app_dir
shortcut.Description = "OpenAmika AI Companion"
shortcut.save()
print("Desktop Shortcut:", os.path.exists(desktop_lnk))

# 2. Startup shortcut (for 24/7 autostart)
shortcut_st = shell.CreateShortCut(startup_lnk)
shortcut_st.Targetpath = "wscript.exe"
shortcut_st.Arguments = f'"{vbs_path}"'
shortcut_st.WorkingDirectory = app_dir
shortcut_st.Description = "OpenAmika AI Companion (Autostart)"
shortcut_st.save()
print("Startup Shortcut (24/7):", os.path.exists(startup_lnk))
