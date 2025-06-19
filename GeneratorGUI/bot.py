#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import win32gui
import win32con

def hide_console():
    console_window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(console_window, win32con.SW_HIDE)

def start_gui():
    try:
        hide_console()  # 在启动 GUI 前隐藏控制台
        from gui_app.voice_gui import launch_gui
        launch_gui()
    except Exception as e:
        print(f"启动GUI失败: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    start_gui()
