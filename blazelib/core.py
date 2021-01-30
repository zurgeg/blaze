import json
import os.path, sys
linux = False
darwin = False
nt = False
if "linux" in sys.platform:
    print("[CORE] [INFO] Detected Environ as GNU/Linux")
    linux = True
    BASE_DIR = "~/.blaze/"
elif "darwin" in sys.platform:
    print("[CORE] [INFO] Detected Environ as Darwin/OS X/macOS")
    darwin = True
    BASE_DIR = "~/.blaze/"
elif "win" in sys.platform:
    print("[CORE] [INFO] Detected Environ as NT")
    nt = True
    BASE_DIR = "%appdata%/Blaze/"
else:
    print("[CORE] [WARNING] Environ is unknown, falling back to GNU/Linux')
    linux = True
    BASE_DIR = "~/.blaze/"
print(f"[CORE] [INFO] Data will be stored at {BASE_DIR}")
current_system_dir = BASE_DIR + "Blaze/Data/Generic"
current_system_icon = BASE_DIR + "Icons/generic.ico"
def load_console(folder=BASE_DIR + "Generic", file_format="rom", name="Blaze Generic Console", icon=BASE_DIR + "Icons/generic.ico", icon_url="some url lol"):
    print("[CORE] [INFO] Loading console")
    if not os.path.exists(folder):
        print("[CORE] [WARNING] Console directory is empty, there will be no manifest!")
        os.path.mkdir(folder)
    raise NotImplementedError
