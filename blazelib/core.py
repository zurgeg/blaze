import json
import os.path, sys
import os
linux = False
darwin = False
nt = False
portable = True
directory_override = 'definitions/'
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
    BASE_DIR = os.path.join(os.environ.get("AppData") + "\\Blaze\\")
else:
    print("[CORE] [WARNING] Environ is unknown, falling back to GNU/Linux")
    linux = True
    BASE_DIR = "~/.blaze/"
if portable:
    BASE_DIR = "blaze_data/"
if directory_override:
    BASE_DIR = directory_override
print(f"[CORE] [INFO] Data will be stored at {BASE_DIR}")
if not os.path.exists(BASE_DIR):
    os.mkdir(BASE_DIR)
current_system_dir = BASE_DIR + "Blaze/Data/Generic"
current_system_icon = BASE_DIR + "Icons/generic.ico"
def load_console(folder=BASE_DIR + "Generic", file_format="rom", name="Blaze Generic Console", icon=BASE_DIR + "Icons/generic.ico", icon_url=None):
    print("[CORE] [INFO] Loading console")
    if not os.path.exists(folder):
        print("[CORE] [WARNING] Console directory is empty, there will be no manifest!")
        os.mkdir(folder)
    print("[CORE] [INFO] Parsing manifest...", end="")
    if not os.path.exists(folder + "/manifest.json"):
          print(f"FAIL\n[{name}] [FATAL] {folder}/manifest.json does not exist!\n[CORE] [ERROR] Console could not load")
          return 1 # A return of 1 means manifest.json is missing
    else:
          manifest = json.load(open(folder + "/manifest.json"))
          try:
              specfile = manifest['cpu_info']
          except KeyError:
              print(f"FAIL\n[{name}] [FATAL] {folder}/manifest.json is missing CPU Info and is invalid!!\n[CORE] [ERROR] Console could not load")
              return 2 # 2 = Invalid Manifest
          finally:
              print(f"OK\n[CORE] [INFO] {name} (at folder {folder}) loaded successfully!")
          if not os.path.exists(folder + f"/{specfile}"):
              print(f"[{name}] [MANIFEST] [ERROR] Specification File does not exists, should be in {specfile}")
              return 3 # 3 = Missing specfile
          else:
              specs = json.load(open(folder + f"/{specfile}"))
              if "import" not in list(specs.keys()):
                  print(f"[{name}] [SPECS] [ERROR] {specfile} is missing \"import\" key and is invalid!!\n[CORE] [ERROR] Console could not load")
                  return 4 # 4 = Invalid CPU Specs
              else:
                  # Everything is all good!
                  print("[CORE] [INFO] Console OK!!")
                  current_system_dir = folder
                  current_system_icon = "Icons/generic.ico"
                  if "mode" in list(specs.keys()):
                      if "mode" == 'lowlevel':
                          return [specs['import'], specs, manifest, folder, file_format, name, icon_url, True]
                  return [specs['import'], specs, manifest, folder, file_format, name, icon_url, False] # This holds console info, it's formatted like so. [functions_file, specs_dict, manifest_dict, folder, file_format, name, icon, icon_url]
             
          
    
