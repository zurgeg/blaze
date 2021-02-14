# Allows hooking into games
import zlib
print('[HOOKS] [INFO] Loading...')
specs = blazelib.libemu.current_console[1]
rom = blazelib.libemu.current_rom
console_name = 'NA'
hooks_enabled = False
features = []
def calculate_flags(features):
    flags = 0
    if 'register' in features:
        flags += 2
    if 'ram' in features:
        flags += 4
    if 'sprite' in features:
        flags += 6
    return flags


if not 'console_name' in list(specs.keys()):
    print('[HOOKS] [WARNING] Current console is unnamed')
    print('[HOOKS] [INFO] To enable hooks that require names')
    print('[HOOKS] [INFO] Place a \'console_name\' value in the console')
else:
    console_name = specs['console_name']
if not 'hooks_enabled' in list(specs.keys()) or not specs['hooks_enabled']:
    print('[HOOKS] [WARNING] Hooks are disabled for this console.')
else:
    hooks_enabled = True
if not 'features' in list(specs.keys()):
    print('[HOOKS] [WARNING] Hooks data invalid. Hooks are disabled')
    hooks_enabled = False
else:
    flags = specs['features']
    if flags >> 1:
        features.append('register')
    if flags >> 2:
        features.append('ram')
    if flags >> 3:
        features.append('sprite')
    if flags >> 4:
        features = []
        hooks_enabled = False
        print('[HOOKS] [WARNING] Hooks data invalid. Hooks are disabled')


