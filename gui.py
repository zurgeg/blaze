import blazelib.libgui
if blazelib.libgui.BACKEND == blazelib.libgui.DEARPYGUI:
    about = '''
    Blaze is a multiplatform emulator designed around portability.
    The developer of Blaze is primarily focused on finishing Blaze for 
    Windows. After that the plan is to port Blaze to CircuitPython, a 
    microcontroller platform that is renouned for it's simplicity
    and portability.

    Version: 0.3-Alpha.
    Backend: Dear PyGUI
    Move this window out of the way to view the main window.
    '''
else:
    about = '''
    Blaze is a multiplatform emulator designed around portability.
    The developer of Blaze is primarily focused on finishing Blaze for 
    Windows. After that the plan is to port Blaze to CircuitPython, a 
    microcontroller platform that is renouned for it's simplicity
    and portability.

    Version: 0.3-Alpha.
    Backend: Tkinter
    '''
backend_settings_window = 'a non existent window :)'
def open_backend_settings(sender, data):
    global backend_settings_window
    blazelib.libgui.delete(backend_settings_window)
    backend_settings_window = blazelib.libgui.make_window('Backend Settings')
    text = blazelib.libgui.make_text('Oh hi! I wasn\'t expecting you here!', window)
    blazelib.libgui.end_container()
def open_about(sender, data):
    blazelib.libgui.delete(aboutwindow)
    window = blazelib.libgui.make_window('About Blaze')
    text = blazelib.libgui.make_text(about, window) 
    blazelib.libgui.end_container()
window = blazelib.libgui.make_window('Blaze')
menu = blazelib.libgui.make_menu(window, 'Main', 'Options')
menu_bar = blazelib.libgui.make_menu_bar(menu,  'MainBar')
menu_item = blazelib.libgui.make_menu_item(menu_bar, 'something', 'Backend', open_backend_settings)
blazelib.libgui.end_container()
menu = blazelib.libgui.make_menu(window, 'help', 'Help')
menu_bar = blazelib.libgui.make_menu_bar(menu, 'HelpBar')
menu_item = blazelib.libgui.make_menu_item(menu_bar, 'about', 'About', open_about)
blazelib.libgui.end_container()
blazelib.libgui.end_container()
aboutwindow = blazelib.libgui.make_window('About Blaze')
text = blazelib.libgui.make_text(about, aboutwindow)
blazelib.libgui.end_container()
blazelib.libgui.start(window)