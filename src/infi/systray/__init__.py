import sys
if sys.version_info < (3,3,0):
    __import__("pkg_resources").declare_namespace(__name__)
from .traybar import SysTrayIcon
