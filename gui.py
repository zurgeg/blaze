import blazelib.libgui, blazelib.libemu, blazelib.core
from threading import Thread, Event
import sys, os
if blazelib.libgui.BACKEND == blazelib.libgui.DEARPYGUI:
    about = '''
    Blaze is a multiplatform emulator designed around portability.
    The developer of Blaze is primarily focused on finishing Blaze for 
    Windows. After that the plan is to port Blaze to CircuitPython, a 
    microcontroller platform that is renouned for it's simplicity
    and portability.

    Version: 0.3-Alpha.
    Backend: Dear PyGUI
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
rom = 'ibm.ch8'
backend_settings_window = 'a non existent window :)'
class State:
    def __init__(self):
        self.stop = Event()
        self.game_thread = Thread(target=self.start_game, args=[self.stop])
    def start_game_thread(self):
        self.game_thread.start()
    def start_game(self, stop):
        console = blazelib.core.load_console(folder=blazelib.core.BASE_DIR + 'chip8', name="BlazeLib CLI Virtual Console")
        blazelib.libemu.threadsafe_exec_rom(rom, 1, console, stop)
    def end_game_thread(self):
        self.stop.set()
        exit()
state = State()
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
def handle_file(sender, data):
    global rom
    rom = os.path.join(data[0], data[1])
def open_selector(sender, data):
    global window
    blazelib.libgui.file_selector(window, handle_file)
def launch_game(sender, data):
    state.start_game_thread()
def quit_command(sender, data):
    state.end_game_thread()
    exit(0)
window = blazelib.libgui.make_window('Blaze')
menu = blazelib.libgui.make_menu(window, 'Main', 'Options')
menu_bar = blazelib.libgui.make_menu_bar(menu,  'MainBar')
menu_item = blazelib.libgui.make_menu_item(menu_bar, 'something', 'Backend', open_backend_settings)
blazelib.libgui.end_container()
menu = blazelib.libgui.make_menu(window, 'help', 'Help')
menu_bar = blazelib.libgui.make_menu_bar(menu, 'HelpBar')
menu_item = blazelib.libgui.make_menu_item(menu_bar, 'about', 'About', open_about)
blazelib.libgui.end_container()
menu = blazelib.libgui.make_menu(window, 'file', 'File')
menu_bar = blazelib.libgui.make_menu_bar(menu, 'FileBar')
menu_item = blazelib.libgui.make_menu_item(menu_bar, 'open', 'Open', open_selector)
blazelib.libgui.end_container()
launch_button = blazelib.libgui.make_button('Play', launch_game, window)
exit_button = blazelib.libgui.make_button('Quit', quit_command, window)
blazelib.libgui.end_container()
aboutwindow = blazelib.libgui.make_window('About Blaze')
text = blazelib.libgui.make_text(about, aboutwindow)
blazelib.libgui.end_container()
blazelib.libgui.start(window)