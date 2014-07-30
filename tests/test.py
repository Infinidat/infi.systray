from __future__ import print_function
from infi.systray import SysTrayIcon
import os
import ctypes

icon_path = os.path.join(os.path.dirname(__file__), "test.ico")
shutdown_called = False
def on_quit(systray):
    print("Bye")
def do_example(systray):
    print("Example")
def on_about(systray):
    ctypes.windll.user32.MessageBoxW(None, u"This is a test of infi.systray", u"About", 0)

menu_options = (("Example", None, do_example),
                ("About", None, on_about))
systray = SysTrayIcon(icon_path, "Systray Test", menu_options, on_quit)
systray.start()