import importlib.util
from binascii import hexlify
import re, json
def read_and_exec(file, offset, n_bytes, console):
    with open(file, 'rb') as file:
        spec = importlib.util.spec_from_file_location("console", f"{console[3]}/{console[0]}")
        console_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(console_module)
        # Now we are done that, and we can read 4 bytes
        file.seek(offset - 1)
        data = file.read(n_bytes)
        data = str(hexlify(data))[2:-1]
        # All done loading data! Now we can call upon our "trusty" partner... RegEx!
        
        
        
        # just kidding i hate regex
        # I just realized we now have to compile every statement in the spec file! *super mario 64 slide music plays*
        # yeeeeeah, probably should've done that beforehand somehow
        spec = console[1]
        for i in spec['patterns']:
            statement = re.compile(list(i.keys())[0])
            if statement.match(data):
                getattr(console_module, list(i.values())[0])() # note: this line is spaghetti, please fix thx
def exec_rom(file, bytes_per_instruction, console):
    with open(file, 'rb') as file:
        spec = importlib.util.spec_from_file_location("console", f"{console[3]}/{console[0]}")
        console_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(console_module)
        # Now we are done that, and we can read 4 bytes
        data = file.read(bytes_per_instruction)
        while data:
            data = str(hexlify(data))[2:-1]
            # All done loading data! Now we can call upon our "trusty" partner... RegEx!
            
            
            
            # just kidding i hate regex
            # I just realized we now have to compile every statement in the spec file! *super mario 64 slide music plays*
            # yeeeeeah, probably should've done that beforehand somehow
            spec = console[1]
            for i in spec['patterns']:
                statement = re.compile(list(i.keys())[0])
                if statement.match(data):
                    getattr(console_module, list(i.values())[0])() # note: this line is spaghetti, please fix thx
            data = file.read(bytes_per_instruction)

    
        
        
