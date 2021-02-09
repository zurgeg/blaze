# Allows GUIs in a platform/module independent way
TK = 0
DEARPYGUI = 1
BACKEND = DEARPYGUI
if BACKEND == TK:
    from tkinter import *
elif BACKEND == DEARPYGUI:
    from dearpygui.simple import *
    from dearpygui.core import *
if BACKEND == TK:
    is_menubar_current_container = False
    print('WARNING: Tkinter backend is deprecated.')
    def make_window(title):
        window = Tk()
        window.title(title)
        return window
    def make_label(text, window):
        l = Label(window, text=text)
        l.pack()
        return l
    def make_button(text, callback, window):
        b = Button(window, command=lambda: callback(None, None), text=text)
        b.pack()
        return b
    def make_menu(window, name, label):
        global is_menubar_current_container
        menubar = Menu(window)
        is_menubar_current_container = label
        return menubar
    def make_menu_bar(window, name):
        global is_menubar_current_container
        menubar = Menu(window)
        is_menubar_current_container = (menubar, is_menubar_current_container, window)
        return menubar
    def make_menu_item(window, name, label, callback):
        window.add_command(label=label, command=callback)
    def make_text(text, window):
        make_label(text, window)
    def start(window):
        window.mainloop()
    def end_container():
        if is_menubar_current_container:
            is_menubar_current_container[2].add_cascade(menu=is_menubar_current_container[0], label=is_menubar_current_container[1])
    def delete(item):
        item.destroy()
elif BACKEND == DEARPYGUI:
    def make_window(title):
        add_window(title)
        return title
    def make_label(text, window):
        add_text(text)
    def make_button(text, callback, window):
        add_button(text, callback=callback)
    def make_menu_bar(window, name):
        add_menu_bar(name)
        return name
    def make_menu(window, name, label):
        add_menu(name, label=label)
        return name
    def make_menu_item(window, name, label, callback):
        add_menu_item(name, callback=callback, label=label)
        return name
    def make_text(text, window):
        add_text(text)
    def start(window):
        show_logger()
        set_log_level(mvTRACE)
        start_dearpygui(primary_window=window)
    def file_selector(window, callback):
        open_file_dialog(callback=callback, extensions=".*")
    def end_container():
        end()
    def delete(item):
        delete_item(item=item)

