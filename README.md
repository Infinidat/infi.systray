Overview
========
This module implements a Windows system tray icon with a right-click context menu.

Installation
------------
To install infi.systray, run:

    pip install infi.systray

Alternatively, you can use easy_install.

Usage
-----
### Creating an icon with one option in the context menu:

    from infi.systray import SysTrayIcon
    def say_hello(systray):
        print "Hello, World!"
    menu_options = (("Say Hello", "hello.ico", say_hello),)
    systray = SysTrayIcon("icon.ico", "Example tray icon", menu_options)
    systray.start()

The first parameter to SysTrayIcon is a path to the icon to show in the systray. If the icon is not found, or
if None is specified, a default system icon will be displayed.
The second parameter is the hover text to show when the mouse is hovered over the systray icon.
The traybar will run in its own thread, so the using script can continue to run.

For the parameters of `menu_options`: cf the section **Menu** below

### Updating : icon, hover text and/or menu options
The icon and/or hover text and/or menu options can be updated using the update() method with the appropriate `hover_text` or `icon` or  `menu_options` keyword argument:

#### Updating the hover_text:

    for item in ['item1', 'item2', 'item3']:
        systray.update(hover_text=item)
        do_something(item)

#### Updating the menu options:

    def say_hello(systray):
        systray.update(menu_options=menu_optionsbye)
    def say_bye(systray):
        systray.update(menu_options=menu_optionshello)
    menu_optionshello = (("Say Hello","hello.ico", say_hello),)
    menu_optionsbye = (("Say Bye", "bye.ico", say_bye),)
    systray = SysTrayIcon("icon.ico", "Hello/Bye", menu_optionshello)   
    systray.start()

### Shutting down
To destroy the icon when the program ends, call

    systray.shutdown()

SysTrayIcon can be used as a context manager to start and shutdown the tray, which also prevents hung tray threads should the parent thread fail or otherwise not close the tray process:

        with SysTrayIcon(icon, hover_text) as systray:
            for item in ['item1', 'item2', 'item3']:
                systray.update(hover_text=item)
                do_something(item)

A "Quit" command is always appended to the end of the icon context menu, after the menu options specified by the user.
To perform operations when Quit is selected, pass "on_quit=callback" as a parameter, e.g.:

    def on_quit_callback(systray):
        program.shutdown()
    systray = SysTrayIcon("icon.ico", "Example tray icon", menu_options, on_quit=on_quit_callback)

### Menu :
#### Parameters

    menu_options = (("Say Hello", "hello.ico", say_hello),)
    
`menu_options` must be a list of 3-tuples. Each 3-tuple specifies a context menu options. 
The first value in each tuple is the context menu string.
The second value is the icon (some versions of Windows can show icons next to each option in the context menu). If None is passed, no icon is displayed for the option 
The third value is the command to execute when the context menu is selected by the user.

#### Default Menu index and Double click 
When the user double-clicks the systray icon, the first option specified in menu_options will be executed. The default
command may be changed to a different option by setting the parameter "default_menu_index", e.g.:

    systray = SysTrayIcon("icon.ico", "Example tray icon", menu_options, default_menu_index=2)

#### Sub-menus

It is possible to create sub-menus in the context menu by recursively passing a list of 3-tuple options as the third
value of an option, instead of passing a callback function. e.g.

    from infi.systray import SysTrayIcon
    hover_text = "SysTrayIcon Demo"
    def hello(sysTrayIcon):
        print "Hello World."
    def simon(sysTrayIcon):
        print "Hello Simon."
    def bye(sysTrayIcon):
        print 'Bye, then.'
    def do_nothing(sysTrayIcon):
        pass
    menu_options = (('Say Hello', "hello.ico", hello),
                    ('Do nothing', None, do_nothing),
                    ('A sub-menu', "submenu.ico", (('Say Hello to Simon', "simon.ico", simon),
                                                   ('Do nothing', None, do_nothing),
                                                  ))
                   )
    sysTrayIcon = SysTrayIcon("main.ico", hover_text, menu_options, on_quit=bye, default_menu_index=1)
    sysTrayIcon.start()

Note that in the previous examples, if no code is executed after calling systray.start(), the main thread will
exit and the icon thread will continue to exist until the Quit option is selected. In order to catch keyboard
interrupts, some code must be written that will call systray.shutdown when the program should quit.
Using SysTrayIcon as a context manager automates the start and shutdown of the tray.

This module can only be used in Windows systems, otherwise the import statement will fail.

Credit
------
This module is adapted from an implementation by Simon Brunning, which in turn was adapted from Mark Hammond's
win32gui_taskbar.py and win32gui_menu.py demos from PyWin32.

Checking out the code
=====================

To run this code from the repository for development purposes, run the following:

    easy_install -U infi.projector
    projector devenv build
