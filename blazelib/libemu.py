import importlib.util
from binascii import hexlify
import re, json
instruction_cache = {} # This caches instructions
# Format: {offset: function}
# TODO: Make exec_rom take advantage of this
current_rom = ''
current_console = []
current_addr = None
base = 0x0
extra_seek = 0
current_file = None
def cache_regex(*args, **kwargs):
    raise NotImplementedError()
def read_and_exec(file, offset, n_bytes, console):
    global base, current_addr
    current_addr = offset
    #base = offset
    with open(file, 'rb') as file:
        spec = importlib.util.spec_from_file_location("console", f"{console[3]}/{console[0]}")
        console_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(console_module)
        # Now we are done that, and we can read 4 bytes
        file.seek(offset)
        data = file.read(n_bytes)
        data = str(hexlify(data))[2:-1]
        # All done loading data! Now we can call upon our "trusty" partner... RegEx!
        
        
        
        # just kidding i hate regex
        # I just realized we now have to compile every statement in the spec file! *super mario 64 slide music plays*
        # yeeeeeah, probably should've done that beforehand somehow
        spec = console[1]
        for i in spec['patterns']:
            statement = re.compile(list(i.keys())[0])
            number_of_arguments = i['args']
            if statement.match(data):
                print(data)
                if 'argument_handler' in list(spec.keys()):
                    if 'arg_handler_kwargs' in list(i.keys()):
                        arguments = getattr(console_module, spec['argument_handler'])(hexlify(file.read(number_of_arguments)), **i['arg_handler_kwargs'])
                    else:
                        arguments = getattr(console_module, spec['argument_handler'])(hexlify(file.read(number_of_arguments)))
                else:
                    arguments = hexlify(file.read(number_of_arguments))
                        
                if "kwargs" in list(i.keys()):   
                    getattr(console_module, list(i.values())[0])(arguments, **i['kwargs']) # note: this line is spaghetti, please fix thx
                else:
                    getattr(console_module, list(i.values())[0])(arguments) # 
def exec_rom(file, bytes_per_instruction, console):
    global current_rom, current_console, current_addr, extra_seek, current_file
    current_rom = file
    current_console = console
    with open(file, 'rb') as file:
        current_file = file
        spec = importlib.util.spec_from_file_location("console", f"{console[3]}/{console[0]}")
        console_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(console_module)
        # Now we are done that, and we can read 4 bytes
        data = 1
        extra_seek = 0
        current_addr = 0
        spec = console[1]
        if 'header_handler' in list(spec.keys()):
            file.read(spec['header_size'])
        while data:
            if data == 1:
                data = file.read(bytes_per_instruction)
            data = str(hexlify(data))[2:-1]
            # All done loading data! Now we can call upon our "trusty" partner... RegEx!
            
            
            
            # just kidding i hate regex
            # I just realized we now have to compile every statement in the spec file! *super mario 64 slide music plays*
            # yeeeeeah, probably should've done that beforehand somehow
            for i in spec['patterns']:
                statement = re.compile(list(i.keys())[0])
                number_of_arguments = i['args']
                if 'pass_instruction' in list(spec.keys()):
                    do_pass_instruction = spec['pass_instruction']
                else:
                    do_pass_instruction = False
                if statement.match(data):
                    print(data)
                    if 'argument_handler' in list(spec.keys()):
                        if 'arg_handler_kwargs' in list(i.keys()):
                            arguments = getattr(console_module, spec['argument_handler'])(hexlify(file.read(number_of_arguments)), **i['arg_handler_kwargs'])
                        else:
                            arguments = getattr(console_module, spec['argument_handler'])(hexlify(file.read(number_of_arguments)))
                    else:
                        arguments = hexlify(file.read(number_of_arguments))
                            
                    if "kwargs" in list(i.keys()):
                        if do_pass_instruction:
                            getattr(console_module, list(i.values())[0])(arguments, data, **i['kwargs']) # note: this line is spaghetti, please fix thx
                        else:
                            getattr(console_module, list(i.values())[0])(arguments, **i['kwargs']) # note: this line is spaghetti, please fix thx
                            
                    else:
                        if do_pass_instruction:
                            getattr(console_module, list(i.values())[0])(arguments, data) #
                        else:
                            getattr(console_module, list(i.values())[0])(arguments)
                            
            data = file.read(bytes_per_instruction)
            current_addr += bytes_per_instruction
            print(current_addr)

    
        
        
