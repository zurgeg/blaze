import sys
import blazelib.libemu, blazelib.core
import os.path
ec = False
if sys.argv[1] == '--help' or sys.argv[1] == '-h':
    print('--Blaze v0.2-Alpha--')
    print('python cli.py OR blaze_cli [ROM or -h/--help] [Console Folder]')
    exit(0)
else:
    print('--Blaze v0.2-Alpha--')
    print('User profile: [Not implemented yet]')
    if not os.path.exists(sys.argv[1]):
      print('[CLI] [FATAL] ROM file does not exist!')
      exit(1)
    else:
      if not os.path.exists(os.path.join(blazelib.core.BASE_DIR, sys.argv[2])):
        print(f'[CLI] [FATAL] Console folder doesn\'t exist! Are you sure it\'s in {blazelib.core.BASE_DIR}?')
        exit(1)
      else:
        console = blazelib.core.load_console(folder=blazelib.core.BASE_DIR + sys.argv[2], name="BlazeLib CLI Virtual Console")
        if ec:
            try:
                blazelib.libemu.exec_rom(sys.argv[1], 1, console)
            except Exception as e:
                print(f'[CLI] [FATAL] Emulator crashed: {e}')
                exit(2)
        else:
            blazelib.libemu.exec_rom(sys.argv[1], 1, console)
        exit(0)
    
    

