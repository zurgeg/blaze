import blazelib.libgui
def clicked(sender, data):
    print('You clicked me!')
window = blazelib.libgui.make_window('Hi!')
label = blazelib.libgui.make_label('This is a test!', window)
button = blazelib.libgui.make_button('Push Me!', clicked, window)
window = blazelib.libgui.make_window('WOW!')
label = blazelib.libgui.make_label('It\'s another window!', window)
blazelib.libgui.start(window)