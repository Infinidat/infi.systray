import os
import sys
from win32_adapter import *
import threading
    
class SysTrayIcon(object):
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]
    
    FIRST_ID = 1023
    
    def __init__(self,
                 icon,
                 hover_text,
                 menu_options,
                 on_quit=None,
                 default_menu_index=None,
                 window_class_name="SysTrayIconPy"):
        
        self.icon = icon
        self.hover_text = hover_text
        self.on_quit = on_quit
        
        menu_options = menu_options + (('Quit', None, self.QUIT),)
        self._next_action_id = self.FIRST_ID
        self.menu_actions_by_id = set()
        self.menu_options = self._add_ids_to_menu_options(list(menu_options))
        self.menu_actions_by_id = dict(self.menu_actions_by_id)
        
        self.default_menu_index = (default_menu_index or 0)
        self.window_class_name = convert_to_ascii(window_class_name)
        self.message_dict = {RegisterWindowMessage("TaskbarCreated"): self._restart,
                             WM_DESTROY: self._destroy,
                             WM_CLOSE: self._destroy,
                             WM_COMMAND: self._command,
                             WM_USER+20 : self._notify,}
        self.notify_id = None
        self.message_loop_thread = None
        self._register_class()

    def set_icon(self, icon=None, hover_text=None):
        """ update icon image and/or hover text """
        if icon:
            self.icon = icon
        if hover_text:
            self.hover_text = hover_text
        self._refresh_icon()

    def WndProc(self, hwnd, msg, wparam, lparam):
        hwnd = HANDLE(hwnd)
        wparam = WPARAM(wparam)
        lparam = LPARAM(lparam)
        if msg in self.message_dict:
            self.message_dict[msg](hwnd, msg, wparam.value, lparam.value)
        return DefWindowProc(hwnd, msg, wparam, lparam)
        
    def _register_class(self):
        # Register the Window class.
        self.window_class = WNDCLASS()
        self.hinst = self.window_class.hInstance = GetModuleHandle(None)
        self.window_class.lpszClassName = self.window_class_name
        self.window_class.style = CS_VREDRAW | CS_HREDRAW;
        self.window_class.hCursor = LoadCursor(0, IDC_ARROW)
        self.window_class.hbrBackground = COLOR_WINDOW
        self.window_class.lpfnWndProc = LPFN_WNDPROC(self.WndProc)
        classAtom = RegisterClass(ctypes.byref(self.window_class))

    def _create_window(self):
        style = WS_OVERLAPPED | WS_SYSMENU
        self.hwnd = CreateWindowEx(0, self.window_class_name,
                                      self.window_class_name,
                                      style,
                                      0,
                                      0,
                                      CW_USEDEFAULT,
                                      CW_USEDEFAULT,
                                      0,
                                      0,
                                      self.hinst,
                                      None)
        UpdateWindow(self.hwnd)
        self._refresh_icon()

    def _message_loop_func(self):
        self._create_window()
        PumpMessages()

    def start(self):
        self.message_loop_thread = threading.Thread(target=self._message_loop_func)
        self.message_loop_thread.start()

    def shutdown(self):
        PostMessage(self.hwnd, WM_CLOSE, 0, 0)
        self.message_loop_thread.join()

    def _add_ids_to_menu_options(self, menu_options):
        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in self.SPECIAL_ACTIONS:
                self.menu_actions_by_id.add((self._next_action_id, option_action))
                result.append(menu_option + (self._next_action_id,))
            elif non_string_iterable(option_action):
                result.append((option_text,
                               option_icon,
                               self._add_ids_to_menu_options(option_action),
                               self._next_action_id))
            else:
                raise Exception('Unknown item', option_text, option_icon, option_action)
            self._next_action_id += 1
        return result
        
    def _refresh_icon(self):
        # Try and find a custom icon
        hicon = 0
        if self.icon is not None and os.path.isfile(self.icon):
            icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE
            icon = convert_to_ascii(self.icon)
            hicon = LoadImage(0,
                              icon,
                              IMAGE_ICON,
                              0,
                              0,
                              icon_flags)
        if hicon == 0:
            # Can't find icon file - using default
            hicon = LoadIcon(0, IDI_APPLICATION)

        if self.notify_id: message = NIM_MODIFY
        else: message = NIM_ADD
        self.notify_id = NotifyData(self.hwnd,
                          0,
                          NIF_ICON | NIF_MESSAGE | NIF_TIP,
                          WM_USER+20,
                          hicon,
                          self.hover_text)
        Shell_NotifyIcon(message, ctypes.byref(self.notify_id))

    def _restart(self, hwnd, msg, wparam, lparam):
        self._refresh_icon()

    def _destroy(self, hwnd, msg, wparam, lparam):
        if self.on_quit: self.on_quit(self)
        nid = NotifyData(self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, ctypes.byref(nid))
        PostQuitMessage(0) # Terminate the app.

    def _notify(self, hwnd, msg, wparam, lparam):
        if lparam == WM_LBUTTONDBLCLK:
            self._execute_menu_option(self.default_menu_index + self.FIRST_ID)
        elif lparam == WM_RBUTTONUP:
            self._show_menu()
        elif lparam == WM_LBUTTONUP:
            pass
        return True
        
    def _show_menu(self):
        menu = CreatePopupMenu()
        self._create_menu(menu, self.menu_options)
        #SetMenuDefaultItem(menu, 1000, 0)
        
        pos = POINT()
        GetCursorPos(ctypes.byref(pos))
        # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
        SetForegroundWindow(self.hwnd)
        TrackPopupMenu(menu,
                       TPM_LEFTALIGN,
                       pos.x,
                       pos.y,
                       0,
                       self.hwnd,
                       None)
        PostMessage(self.hwnd, WM_NULL, 0, 0)
    
    def _create_menu(self, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_icon:
                option_icon = self._prep_menu_icon(option_icon)
            
            if option_id in self.menu_actions_by_id:                
                item = PackMENUITEMINFO(text=option_text,
                                        hbmpItem=option_icon,
                                        wID=option_id)
                InsertMenuItem(menu, 0, 1, ctypes.byref(item))
            else:
                submenu = CreatePopupMenu()
                self._create_menu(submenu, option_action)
                item = PackMENUITEMINFO(text=option_text,
                                        hbmpItem=option_icon,
                                        hSubMenu=submenu)
                InsertMenuItem(menu, 0, 1,  ctypes.byref(item))

    def _prep_menu_icon(self, icon):
        icon = convert_to_ascii(icon)
        # First load the icon.
        ico_x = GetSystemMetrics(SM_CXSMICON)
        ico_y = GetSystemMetrics(SM_CYSMICON)
        hicon = LoadImage(0, icon, IMAGE_ICON, ico_x, ico_y, LR_LOADFROMFILE)

        hdcBitmap = CreateCompatibleDC(0)
        hdcScreen = GetDC(0)
        hbm = CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = SelectObject(hdcBitmap, hbm)
        # Fill the background.
        brush = GetSysColorBrush(COLOR_MENU)
        FillRect(hdcBitmap, ctypes.byref(RECT(0, 0, 16, 16)), brush)
        # unclear if brush needs to be feed.  Best clue I can find is:
        # "GetSysColorBrush returns a cached brush instead of allocating a new
        # one." - implies no DeleteObject
        # draw the icon
        DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, DI_NORMAL)
        SelectObject(hdcBitmap, hbmOld)
        DeleteDC(hdcBitmap)
        
        return hbm

    def _command(self, hwnd, msg, wparam, lparam):
        id = LOWORD(wparam)
        self._execute_menu_option(id)
        
    def _execute_menu_option(self, id):
        menu_action = self.menu_actions_by_id[id]
        if menu_action == self.QUIT:
            DestroyWindow(self.hwnd)
        else:
            menu_action(self)
            
def non_string_iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return not isinstance(obj, str)
