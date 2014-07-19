import ctypes

RegisterWindowMessage = ctypes.windll.user32.RegisterWindowMessageW
LoadCursor = ctypes.windll.user32.LoadCursorW
LoadIcon = ctypes.windll.user32.LoadIconW
LoadImage = ctypes.windll.user32.LoadImageW
RegisterClass = ctypes.windll.user32.RegisterClassW
CreateWindowEx = ctypes.windll.user32.CreateWindowExW
UpdateWindow = ctypes.windll.user32.UpdateWindow
DefWindowProc = ctypes.windll.user32.DefWindowProcW
GetSystemMetrics = ctypes.windll.user32.GetSystemMetrics
InsertMenuItem = ctypes.windll.user32.InsertMenuItemW
PostMessage = ctypes.windll.user32.PostMessageW
PostQuitMessage = ctypes.windll.user32.PostQuitMessage
SetMenuDefaultItem = ctypes.windll.user32.SetMenuDefaultItem
GetCursorPos = ctypes.windll.user32.GetCursorPos
SetForegroundWindow = ctypes.windll.user32.SetForegroundWindow
TrackPopupMenu = ctypes.windll.user32.TrackPopupMenu
CreatePopupMenu = ctypes.windll.user32.CreatePopupMenu
CreateCompatibleDC = ctypes.windll.gdi32.CreateCompatibleDC
GetDC = ctypes.windll.user32.GetDC
CreateCompatibleBitmap = ctypes.windll.gdi32.CreateCompatibleBitmap
GetSysColorBrush = ctypes.windll.user32.GetSysColorBrush
FillRect = ctypes.windll.user32.FillRect
DrawIconEx = ctypes.windll.user32.DrawIconEx
SelectObject = ctypes.windll.gdi32.SelectObject
DeleteDC = ctypes.windll.gdi32.DeleteDC
DestroyWindow = ctypes.windll.user32.DestroyWindow
GetModuleHandle = ctypes.windll.kernel32.GetModuleHandleW
GetMessage = ctypes.windll.user32.GetMessageW
TranslateMessage = ctypes.windll.user32.TranslateMessage
DispatchMessage = ctypes.windll.user32.DispatchMessageW
Shell_NotifyIcon = ctypes.windll.shell32.Shell_NotifyIconW
DestroyIcon = ctypes.windll.user32.DestroyIcon

NIM_ADD = 0
NIM_MODIFY = 1
NIM_DELETE = 2
NIF_ICON = 2
NIF_MESSAGE = 1
NIF_TIP = 4
MIIM_ID = 2
MIIM_SUBMENU = 0x004
MIIM_STRING = 0x040
MIIM_BITMAP = 0x080
WM_NULL = 0x000
WM_DESTROY = 0x002
WM_CLOSE = 0x010
WM_COMMAND = 0x111
WM_LBUTTONUP = 0x202
WM_LBUTTONDBLCLK = 0x203
WM_RBUTTONUP = 0x205
WM_USER = 0x400
CS_VREDRAW = 1
CS_HREDRAW = 2
IDC_ARROW = 0x7F00
COLOR_WINDOW = 5
WS_OVERLAPPED = 0
WS_SYSMENU = 0x80000
CW_USEDEFAULT = -0x80000000
LR_LOADFROMFILE = 0x10
LR_DEFAULTSIZE = 0x40
IMAGE_ICON = 1
IDI_APPLICATION = 0x7F00
TPM_LEFTALIGN = 0
SM_CXSMICON = 49
SM_CYSMICON = 50
COLOR_MENU = 4
DI_NORMAL = 3

# WPARAM is defined as UINT_PTR (unsigned type)
# LPARAM is defined as LONG_PTR (signed type)
if ctypes.sizeof(ctypes.c_long) == ctypes.sizeof(ctypes.c_void_p):
    WPARAM = ctypes.c_ulong
    LPARAM = ctypes.c_long
    LRESULT = ctypes.c_long
elif ctypes.sizeof(ctypes.c_longlong) == ctypes.sizeof(ctypes.c_void_p):
    WPARAM = ctypes.c_ulonglong
    LPARAM = ctypes.c_longlong
    LRESULT = ctypes.c_longlong
HANDLE = ctypes.c_void_p

def convert_to_unicode(s):
    try:
        return s.decode("utf-8")
    except AttributeError:
        return s

LPFN_WNDPROC = ctypes.CFUNCTYPE(LRESULT, HANDLE, ctypes.c_uint, WPARAM, LPARAM)
class WNDCLASS(ctypes.Structure):
    _fields_ = [("style", ctypes.c_uint),
                ("lpfnWndProc", LPFN_WNDPROC),
                ("cbClsExtra", ctypes.c_int),
                ("cbWndExtra", ctypes.c_int),
                ("hInstance", HANDLE),
                ("hIcon", HANDLE),
                ("hCursor", HANDLE),
                ("hbrBackground", HANDLE),
                ("lpszMenuName", ctypes.c_wchar_p),
                ("lpszClassName", ctypes.c_wchar_p),
               ]

class POINT(ctypes.Structure):
    _fields_ = [('x', ctypes.c_long), ('y', ctypes.c_long)]

class RECT(ctypes.Structure):
    _fields_ = [('left', ctypes.c_long), ('top', ctypes.c_long),
                ('right', ctypes.c_long), ('bottom', ctypes.c_long)]

class MENUITEMINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint),
                ("fMask", ctypes.c_uint),
                ("fType", ctypes.c_uint),
                ("fState", ctypes.c_uint),
                ("wID", ctypes.c_uint),
                ("hSubMenu", HANDLE),
                ("hbmpChecked", HANDLE),
                ("hbmpUnchecked", HANDLE),
                ("dwItemData", ctypes.c_void_p),
                ("dwTypeData", ctypes.c_wchar_p),
                ("cch", ctypes.c_uint),
                ("hbmpItem", HANDLE),
               ]

class MSG(ctypes.Structure):
    _fields_ = [("hwnd", HANDLE),
                ("message", ctypes.c_uint),
                ("wParam", WPARAM),
                ("lParam", LPARAM),
                ("time", ctypes.c_ulong),
                ("pt", POINT),
               ]

class NOTIFYICONDATA(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint),
                ("hWnd", HANDLE),
                ("uID", ctypes.c_uint),
                ("uFlags", ctypes.c_uint),
                ("uCallbackMessage", ctypes.c_uint),
                ("hIcon", HANDLE),
                ("szTip", ctypes.c_wchar * 128),
                ("dwState", ctypes.c_uint),
                ("dwStateMask", ctypes.c_uint),
                ("szInfo", ctypes.c_wchar * 256),
                ("uTimeout", ctypes.c_uint),
                ("szInfoTitle", ctypes.c_wchar * 64),
                ("dwInfoFlags", ctypes.c_uint),
                ("guidItem", ctypes.c_char * 16),
                ("hBalloonIcon", HANDLE),
               ]

def PackMENUITEMINFO(text=None, hbmpItem=None, wID=None, hSubMenu=None):
    res = MENUITEMINFO()
    res.cbSize = ctypes.sizeof(res)
    res.fMask = 0
    if hbmpItem is not None:
        res.fMask |= MIIM_BITMAP
        res.hbmpItem = hbmpItem
    if wID is not None:
        res.fMask |= MIIM_ID
        res.wID = wID
    if text is not None:
        text = convert_to_unicode(text)
        res.fMask |= MIIM_STRING
        res.dwTypeData = text
    if hSubMenu is not None:
        res.fMask |= MIIM_SUBMENU
        res.hSubMenu = hSubMenu
    return res

def LOWORD(w):
    return w & 0xFFFF

def PumpMessages():
    msg = MSG()
    while GetMessage(ctypes.byref(msg), None, 0, 0) > 0:
        TranslateMessage(ctypes.byref(msg))
        DispatchMessage(ctypes.byref(msg))

def NotifyData(hWnd=0, uID=0, uFlags=0, uCallbackMessage=0, hIcon=0, szTip=""):
    szTip = convert_to_unicode(szTip)
    res = NOTIFYICONDATA()
    res.cbSize = ctypes.sizeof(res)
    res.hWnd = hWnd
    res.uID = uID
    res.uFlags = uFlags
    res.uCallbackMessage = uCallbackMessage
    res.hIcon = hIcon
    res.szTip = szTip
    return res
