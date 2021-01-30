import importlib.util
from binascii import hexlify
import re, json
<<<<<<< Updated upstream
def read_and_exec(file, offset, console):
    with file as open(file):
        spec = importlib.util.spec_from_file_location("console", console[0])
        console_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(console_module)
        # Now we are done that, and we can read 4 bytes
        data = []
        data.append(file.read(offset))
        data.append(file.read(offset + 1))
        data.append(file.read(offset + 2))
        data.append(file.read(offset + 3))
        data = binascii.hexlify(''.join(data))
=======
def read_and_exec(file, offset, n_bytes, console):
    with open(file, 'rb') as file:
        spec = importlib.util.spec_from_file_location("console", f"{console[3]}/{console[0]}")
        console_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(console_module)
        # Now we are done that, and we can read 4 bytes
        file.seek(offset - 1)
        data = file.read(n_bytes)
        data = str(hexlify(data))[2:-1]
>>>>>>> Stashed changes
        # All done loading data! Now we can call upon our "trusty" partner... RegEx!
        
        
        
        # just kidding i hate regex
        # I just realized we now have to compile every statement in the spec file! *super mario 64 slide music plays*
        # yeeeeeah, probably should've done that beforehand somehow
        spec = json.load(console[1])
        for i in spec['patterns']:
            statement = re.compile(list(i.keys())[0])
            if statement.match(data):
                console_module.__getattr__(list(i.values()[0]))() # note: this line is spaghetti, please fix thx
        
        
        
