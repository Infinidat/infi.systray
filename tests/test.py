from simplesystray import SysTrayIcon

hover_text = "SysTrayIcon Demo"


def hello(sysTrayIcon):
    print("Hello World.")


def simon(sysTrayIcon):
    print("Hello Simon.")


def bye(sysTrayIcon):
    print('Bye, then.')


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
