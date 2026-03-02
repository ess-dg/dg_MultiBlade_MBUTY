#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 14:28:31 2026

@author: essdaq
"""

import os
import stat

# --- Configuration ---
APP_NAME = "MBUTY GUI"
SCRIPT_NAME = "MBUTY_GUI.py"
# Pointing specifically to your logo path
ICON_PATH = os.path.expanduser("~/mbuty/MBUTYcap/GUI/logos/MBlogo.png")

# Automatically gets the full path to your current folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_PATH = os.path.join(BASE_DIR, SCRIPT_NAME)
DESKTOP_PATH = os.path.expanduser("~/Desktop/mbuty.desktop")

# --- Verification ---
if not os.path.exists(ICON_PATH):
    print(f"⚠️ Warning: Icon not found at {ICON_PATH}")
    # Fallback to a system icon if yours is missing
    ICON_PATH = "utilities-terminal"

# --- The Content of the .desktop file ---
desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={APP_NAME}
Comment=Launch MBUTY Control GUI
Exec=python3 {SCRIPT_PATH}
Path={BASE_DIR}
Icon={ICON_PATH}
Terminal=true
Categories=Application;Development;
"""

def create_shortcut():
    try:
        # 1. Write the file to the Desktop
        with open(DESKTOP_PATH, "w") as f:
            f.write(desktop_content)
        
        # 2. Make it executable (chmod +x)
        st = os.stat(DESKTOP_PATH)
        os.chmod(DESKTOP_PATH, st.st_mode | stat.S_IEXEC)
        
        print(f"✅ Success! Shortcut created at: {DESKTOP_PATH}")
        print(f"🖼️  Icon set to: {ICON_PATH}")
        print("\n👉 Final Step: Right-click the icon on your Desktop and select 'Allow Launching'.")
        
    except Exception as e:
        print(f"❌ Failed to create shortcut: {e}")

if __name__ == "__main__":
    create_shortcut()