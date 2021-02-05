class CPU:
    def __init__(self):
        self.ram = [0] * 0x4000
        self.stack = []
        self.delay_timer = 60
        self.sound_timer = 60
        self.x = [0] * 0xF
        self.y = [0] * 0xF
cpu = CPU()
def clear_screen():
    ...
def return_from_subroutine():
    ...
def exec_subroutine(arguments, instruction):
    if arguments == 'e0':
        clear_screen()
    if arguments == 'ee':
        return_from_subroutine()
    address = instruction[1] + str(arguments)[2:-1]
    print(f'Machine Language Subroutine {address}')
def jump_to(arguments, instruction):
    ...
def set_register(arguments, instruction):
    print(f'Set Register V{instruction[1]}')
    index = int(instruction[1], base=16)
    cpu.x[index] = int(arguments, base=16)

    
        
        
