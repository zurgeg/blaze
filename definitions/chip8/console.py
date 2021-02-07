from pygame import draw as pdraw
from pygame import Surface
import pygame.display
import blazelib.libemu
size = (320, 160)
screen = pygame.display.set_mode(size)      
class CPU:
    def __init__(self):
        self.ram = [0] * 0x1FF
        self.rom = open(blazelib.libemu.current_rom, 'rb').read()
        self.stack = []
        self.delay_timer = 60
        self.sound_timer = 60
        self.x = [0] * 0x10
        self.i = 0
        self.screen_array = [[0] * 64] * 32
    def read(self, address):
        if address <= 0x1FF:
            return self.ram[address]
        elif address >= 0x200:
            return self.rom[address - 0x200]
cpu = CPU()    
def exec_subroutine(arguments, instruction):
    if arguments == 'e0':
        clear_screen()
    address = int(instruction, base=16) & 0x0FFF
    print(f'Clear Screen')
def jump_to(arguments, instruction):
    address = int(instruction[1:3], base=16)
    print(f'Jump {address}')
    blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, address, 1, blazelib.libemu.current_console)
def set_register(arguments, instruction):
    print(f'Set Register V{instruction[1]}')
    index = int(instruction[1], base=16) & 0x0F00
    cpu.x[index] = int(arguments, base=16)
def add_to_register(arguments, instruction):
    print(f'Set Register V{instruction[1]}')
    index = int(instruction[1], base=16) & 0x0F00
    cpu.x[index] += int(arguments, base=16)
def draw_chip8(arguments, instruction):
    '''
    print('X ' + str(int(instruction, base=16) & 0x0F00))
    x_pos = cpu.x[(int(instruction, base=16) & 0x0F00)]
    print('Y ' + str((int(instruction, base=16) & 0x00F0) - 1))
    y_pos = cpu.x[(int(instruction, base=16) & 0x00F0) - 1]
    '''
    x_pos = cpu.x[int(instruction[1], 16)]
    y_pos = cpu.x[int(instruction[2], 16)]
    print(f'Draw {x_pos}, {y_pos}')
    x = 0
    y = 0
    sprite_data = 0
    cpu.x[0xF] = 0
    height = int(instruction, base=16) & 0x000F
    for y in range(height):
        print(f'Sprite data is at {cpu.i + y}')
        sprite_data = bin(cpu.read(cpu.i + y))
        sprite_data = sprite_data[2:].zfill(8)
        y_coord = y_pos + y
        print(f'Sprite Data {cpu.i}')
        for x in range(8):
            print(x)
            data = int(sprite_data[x])
            x_coord = x_pos + x
            if data:
                data = 255
            else:
                data = 0
            draw(x_coord, y_coord, data)
def carries(number1, number2):
    num1 = str(number1)
    num2 = str(number2)
    l = len(num1)
    l1 = len(num2)
    carry = 0
    carries = 0
    c1 = l
    c2 = l
    if (l < l1):
        while (c1 < l1):
            num1 = '0' + num1
            c1+=1
    if (l1 < l):
        while (c2 < l):
            num2 = '0' + num2
            c2+=1
    i = c1
    while (i > 0):
        if (int(num1[i-1])+int(num2[i-1])+carry > 9):
            carry = 1;
            carries+=1
        else:
            carry = 0
        i-=1
    return carries != 0
def xor(a, b):
    return (a and not b) or (not a and b)
def draw(xpos, ypos, color):
    x_base = xpos * 5
    y_base = ypos * 5
    pdraw.rect(screen,
              (color, color, color),
              (x_base, y_base, 5, 5))
    pygame.display.flip()
    #cpu.screen_array[ypos][xpos] = color
def set_i(args, instruction):
    print('Set I')
    value = int(instruction, base=16) & 0x0FFF
    cpu.i = value
    print(cpu.i)
def store_y_in_x(args, instruction):
    print(args)
    print(instruction)
    y = int(instruction[2], 16)
    x = int(instruction[1], 16)
    print(f'Store V{y} in V{x}')
    cpu.x[x] = cpu.x[y]
def vx_or_vy(args, instruction):
    y = int(instruction[2], base=16)
    x = int(instruction[1], base=16)
    cpu.x[x] = cpu.x[x] | cpu.x[y]
def vx_and_vy(args, instruction):
    y = int(instruction[2], base=16)
    x = int(instruction[1], base=16)
    cpu.x[x] = x & y
def vx_xor_vy(args, instruction):
    y = int(instruction[2], base=16)
    x = int(instruction[1], base=16)
    cpu.x[x] = xor(x, y)  
def add_carry(args, instruction):
    y = int(instruction[2], base=16)
    x = int(instruction[1], base=16)
    cpu.x[0xF] = int(carries(x, y))    
def sub_carry(args, instruction):
    pass
def add_carry_changed(args, instruction):
    pass
def sub_carry_changed(args, instruction):
    pass
def left_shift(args, instruction):
    pass
def instruction_8(args, instruction):
    final_arg_byte = int(str(args)[2:-1][1], 16)
    if final_arg_byte == 0x0:
        store_y_in_x(args, instruction)
    elif final_arg_byte == 0x1:
        vx_or_vy(args, instruction)
    elif final_arg_byte == 0x2:
        vx_and_vy(args, instruction)
    elif final_arg_byte == 0x3:
        vx_xor_vy(args, instruction)
    elif final_arg_byte == 0x4:
        add_carry(args, instruction)
    elif final_arg_byte == 0x5:
        sub_carry(args, instruction)
    elif final_arg_byte == 0x6:
        add_carry_changed(args, instruction)
    elif final_arg_byte == 0x7:
        sub_carry_changed(args, instruction)
    elif final_arg_byte == 0x8:
        left_shift(args, instruction)
    else:
        print(f'Unknown 8 instruction {final_arg_byte}')
def jump_with_v0(args, instruction):
    addr = int(instruction, base=16) & 0x0FFF
    addr += cpu.x[0]
    print(f'Jump {addr}')
    blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, addr, 1, blazelib.libemu.current_console)
def random_number(args, instruction):
    pass
def instruction_f(args, instruction):
    pass
        
    
        
        
