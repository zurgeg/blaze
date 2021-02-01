import blazelib.libemu
from time import sleep
# Offset libemu reads
blazelib.libemu.base = 0xF
instructionmodes = [
	2, 2, 0, 0, 2, 2, 2, 0, 1, 2, 1, 0, 3, 3, 3, 0,
	2, 2, 0, 0, 2, 2, 2, 0, 1, 3, 1, 0, 3, 3, 3, 0,
	3, 2, 0, 0, 2, 2, 2, 0, 1, 2, 1, 0, 3, 3, 3, 0,
	2, 2, 0, 0, 2, 2, 2, 0, 1, 3, 1, 0, 3, 3, 3, 0,
	1, 2, 0, 0, 2, 2, 2, 0, 1, 2, 1, 0, 3, 3, 3, 0,
	2, 2, 0, 0, 2, 2, 2, 0, 1, 3, 1, 0, 3, 3, 3, 0,
	1, 2, 0, 0, 2, 2, 2, 0, 1, 2, 1, 0, 3, 3, 3, 0,
	2, 2, 0, 0, 2, 2, 2, 0, 1, 3, 1, 0, 3, 3, 3, 0,
	2, 2, 0, 0, 2, 2, 2, 0, 1, 0, 1, 0, 3, 3, 3, 0,
	2, 2, 0, 0, 2, 2, 2, 0, 1, 3, 1, 0, 0, 3, 0, 0,
	2, 2, 2, 0, 2, 2, 2, 0, 1, 2, 1, 0, 3, 3, 3, 0,
	2, 2, 0, 0, 2, 2, 2, 0, 1, 3, 1, 0, 3, 3, 3, 0,
	2, 2, 0, 0, 2, 2, 2, 0, 1, 2, 1, 0, 3, 3, 3, 0,
	2, 2, 0, 0, 2, 2, 2, 0, 1, 3, 1, 0, 3, 3, 3, 0,
	2, 2, 0, 0, 2, 2, 2, 0, 1, 2, 1, 0, 3, 3, 3, 0,
	2, 2, 0, 0, 2, 2, 2, 0, 1, 3, 1, 0, 3, 3, 3, 0,
]
instructionnames = [
	"BRK", "ORA", "KIL", "SLO", "NOP", "ORA", "ASL", "SLO",
	"PHP", "ORA", "ASL", "ANC", "NOP", "ORA", "ASL", "SLO",
	"BPL", "ORA", "KIL", "SLO", "NOP", "ORA", "ASL", "SLO",
	"CLC", "ORA", "NOP", "SLO", "NOP", "ORA", "ASL", "SLO",
	"JSR", "AND", "KIL", "RLA", "BIT", "AND", "ROL", "RLA",
	"PLP", "AND", "ROL", "ANC", "BIT", "AND", "ROL", "RLA",
	"BMI", "AND", "KIL", "RLA", "NOP", "AND", "ROL", "RLA",
	"SEC", "AND", "NOP", "RLA", "NOP", "AND", "ROL", "RLA",
	"RTI", "EOR", "KIL", "SRE", "NOP", "EOR", "LSR", "SRE",
	"PHA", "EOR", "LSR", "ALR", "JMP", "EOR", "LSR", "SRE",
	"BVC", "EOR", "KIL", "SRE", "NOP", "EOR", "LSR", "SRE",
	"CLI", "EOR", "NOP", "SRE", "NOP", "EOR", "LSR", "SRE",
	"RTS", "ADC", "KIL", "RRA", "NOP", "ADC", "ROR", "RRA",
	"PLA", "ADC", "ROR", "ARR", "JMP", "ADC", "ROR", "RRA",
	"BVS", "ADC", "KIL", "RRA", "NOP", "ADC", "ROR", "RRA",
	"SEI", "ADC", "NOP", "RRA", "NOP", "ADC", "ROR", "RRA",
	"NOP", "STA", "NOP", "SAX", "STY", "STA", "STX", "SAX",
	"DEY", "NOP", "TXA", "XAA", "STY", "STA", "STX", "SAX",
	"BCC", "STA", "KIL", "AHX", "STY", "STA", "STX", "SAX",
	"TYA", "STA", "TXS", "TAS", "SHY", "STA", "SHX", "AHX",
	"LDY", "LDA", "LDX", "LAX", "LDY", "LDA", "LDX", "LAX",
	"TAY", "LDA", "TAX", "LAX", "LDY", "LDA", "LDX", "LAX",
	"BCS", "LDA", "KIL", "LAX", "LDY", "LDA", "LDX", "LAX",
	"CLV", "LDA", "TSX", "LAS", "LDY", "LDA", "LDX", "LAX",
	"CPY", "CMP", "NOP", "DCP", "CPY", "CMP", "DEC", "DCP",
	"INY", "CMP", "DEX", "AXS", "CPY", "CMP", "DEC", "DCP",
	"BNE", "CMP", "KIL", "DCP", "NOP", "CMP", "DEC", "DCP",
	"CLD", "CMP", "NOP", "DCP", "NOP", "CMP", "DEC", "DCP",
	"CPX", "SBC", "NOP", "ISC", "CPX", "SBC", "INC", "ISC",
	"INX", "SBC", "NOP", "SBC", "CPX", "SBC", "INC", "ISC",
	"BEQ", "SBC", "KIL", "ISC", "NOP", "SBC", "INC", "ISC",
	"SED", "SBC", "NOP", "ISC", "NOP", "SBC", "INC", "ISC",
]
class RAM:
    def __init__(self):
        self.ram = [0] * 65535
    def read_8(self, offset):
        return self.ram[offset]
    def read_16(self, offset):
        return self.ram[offset:offset+1]
    def write_8(self, offset, data):
        self.ram[offset] = data
    def write_16(self, offset, data):
        self.ram[offset:offset+1] = data
    def ramdump(self):
        # please no
        return self.ram
    def clear_ram(self):
        self.ram = [0] * 65535
class CPU:
    def __init__(self):
        self.ram = RAM()
        self.cycles = 0
        self.sp = 0xFD
        self.a = 0
        self.x = 0
        self.y = 0
        self.c = 0
        self.d = 0
        self.z = 0
        self.i = 0
        self.b = 0
        self.u = 0
        self.v = 0
        self.n = 0
        self.interrupt = None
        self.stall = 100
        self.cycles = 0
    def set_register(self, register, value):
        setattr(self, register, value)
    def get_register(self, register):
        return getattr(self, register)
    def reset(self):
        self.__init__()
    def cycle(self):
        sleep(0.001*self.stall)# We can only cycle every self.stall * 0.001 seconds
        self.cycles += 1
        print(self.regdump())
    def push(self, value):
        self.ram.write_8(0x100|cpu.sp, value)
    def push_16(self, value):
        hi = value >> 8
        lo = value & 0xFF
        self.push(hi)
        self.push(lo)
    def pull():
        self.SP += 1
        return self.ram.read(0x100 | cpu.SP)
    def pull_16():
        lo = cpu.pull()
        hi = cpu.pull()
        return hi<<8 | lo
    def regdump(self):
        return [self.a, self.x, self.y, self.c, self.z, self.i, self.b, self.n, self.v]
    def flags(self):
        flags = 0
        flags |= cpu.c << 0
        flags |= cpu.z << 1
        flags |= cpu.i << 2
        flags |= cpu.d << 3
        flags |= cpu.b << 4
        flags |= cpu.u << 5
        flags |= cpu.v << 6
        flags |= cpu.n << 7
        return flags
    def branchcycles(self, address):
        cpu.cycle()
        if blazelib.libemu.current_addr&0xFF00 != address&0xFF00:
            cpu.cycle()
        
class PPU:
    def __init__(self):
        self.cycle = 0
        self.scanline = 0
        self.frame = 0
        self.palette_data = []
        self.name_table_data = None
        self.v = 0
        self.t = 0
        self.x = 0
        self.w = 0
        self.f = 0

        self.register = 0

        self.nmi_occured = False
        self.nmi_output = False
        self.nmi_previous = False
        self.nmi_delay = 0

        self.name_table_byte = 0
        self.attribute_table_byte = 0
        self.low_tile_byte = 0
        self.high_tile_byte = 0
        self.tile_data = 0

        self.sprite_count = 0
        self.sprite_patterns = 0
        self.sprite_positions = 0
        self.sprite_proiorities = 0
        self.sprite_indexes = 0

        self.flag_name_table = 0
        self.flag_increment = 0
        self.flag_sprite_table = 0
        self.flag_background_table = 0

        self.flag_grayscale = 0
        self.flag_show_left_background = 0
        self.flag_show_left_sprites = 0
        self.flag_show_background = 0
        self.flag_show_sprites = 0
        self.flag_red_tint = 0
        self.flag_green_tint = 0
        self.flag_blue_tint = 0

        self.flag_sprite_zero_hit = 0
        self.flag_sprite_overflow = 0

        self.oam_address = 0
        self.oam_data = []

        self.buffered_data = 0
    def read_palette(self, address):
        if address >= 16 and address%4 == 0:
            address -= 16
        return self.palette_data[address]
    def write_palette(self, address, value):
        if address >= 16 and address%4 == 0:
            address -= 16
        self.palette_data[address] = value
    def read_register(self, address):
        if address == 0x2002:
            return self.read_status()
        elif address == 0x2004:
            return self.read_oam_data()
        elif address == 0x2007:
            return self.read_data()
        return 0
    def write_register(self, address, value):
        self.register = value
        if address == 0x2000:
            self.write_control(value)
        elif address == 0x2001:
            self.write_mask(value)
        elif address == 0x2003:
            self.write_oam_address(value)
        elif address == 0x2004:
            self.write_oam_data(value)
        elif address == 0x2005:
            self.write_scroll(value)
        elif address == 0x2006:
            self.write_address(value)
        elif address == 0x2007:
            self.write_data(value)
        elif address == 0x4014:
            self.write_dma(value)
    def write_control(self, value):
        self.flag_name_table = (value >> 0) & 3
        self.flag_increment = (value >> 2) & 1
        self.flag_sprite_table = (value >> 3) & 1
        self.flag_background_table = (value >> 4) & 1
        self.flag_sprite_size = (value >> 5) & 1
        self.flag_master_slave = (value >> 6) & 1
        self.nmi_output = (value >> 7) & 1 == 1
        self.nmi_change()
        self.t = (self.t & 0xF3FF) | ((value & 0x03) << 10)
    def write_mask(self,value):
        self.flag_grayscale = (value >> 0) & 1
        self.flag_show_left_backgroound = (value >> 1) & 1
        self.flag_show_left_sprites = (value >> 2) & 1
        self.flag_show_background = (value >> 3) & 1
        self.flag_show_sprites = (value >> 4) & 1
        self.flag_red_tint = (value >> 5) & 1
        self.flag_blue_tint = (value >> 6) & 1
        self.flag_green_tint = (value > 7) & 1
    def read_status(self):
        result = self.register & 0x1F
        result |= self.flag_sprite_overflow << 5
        result |= self.flag_sprite_zero_hir << 6
        if self.nmi_occured:
            result |= 1 << 7
        self.nmi_occured = False
        self.nmi_change()
        self.w = 0
        return result
    def write_oam_address(self, value):
        self.oam_address = value
    def read_oam_data(self):
        return self.oam_data[self.oam_address]
    def write_oam_data(self):
        self.oam_data[self.oam_address] = value
        self.oam_address += 1
    # etc., etc., etc.,
    def increment_x(self):
        if self.v&0x001F == 31:
            self.v &= 0xFFE0
            self.v ^= 0x0400
        else:
            self.v += 1
    def increment_y(self):
        if self.v&0x7000 != 0x7000:
            self.v += 0x1000
        else:
            self.v &= 0x8FFF
            y = (self.v & 0x03E0) >> 5
            if y == 29:
                y = 0
                self.v ^= 0x0800
            elif y == 31:
                y = 0
            else:
                y += 1
            self.v = (self.v & 0xFC1F) | (y << 5) 
            
        
cpu = CPU()
ppu = PPU()
class STPException(Exception):
    ...
def notbreak(*args):
    cpu.cycle()
    cpu.push_16(blazelib.libemu.current_addr)
    cpu.push(cpu.flags() | 0x10)
    cpu.set_register('i', 1)
    blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, 0xFFEE, 4, blazelib.libemu.current_console)
    #print('break!'))
def ora(*args):
    cpu.cycle()
    #print('ORA instruction')
def stp(*args):
    cpu.cycle()
    #print('STP instruction. Stop maybe?')
    #raise STPException('Halt.')
def jump_to(address):
    #print(f'Jumping to {address}')
    blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int('0x' + str(address)[2:-1], base=8), 4, blazelib.libemu.current_console)
def adc(address):
    #print('ADC')
    cpu.cycle()
    a = cpu.get_register('a')
    b = cpu.ram.read_8(address)
    c = cpu.get_register('c')
    cpu.set_register('a', a+b+c)
    cpu.set_register('z', a)
    cpu.set_register('n', a)
    if int(a)+int(b)+int(c) > 0xFF:
        cpu.set_register('c',1)
    else:
        cpu.set_register('c', 0)
    if (a^b)&0x80 == 0 and (a^cpu.get_register('a'))&0x80 != 0:
        cpu.set_register('v', 1)
    else:
        cpu.set_register('v', 0)
def notand(address):
    cpu.cycle()
    cpu.set_register('x', cpu.ram.read_8(int(b'0x' + address, base=0)))
    cpu.set_register('a', cpu.get_register('a') & cpu.ram.read_8(int(b'0x' + address, base=0)))
    cpu.set_register('z', cpu.get_register('a'))
    cpu.set_register('n', cpu.get_register('a'))
def asl(address):
    cpu.cycle()
    cpu.set_register('c', (cpu.get_register('a') >> 7) & 1)
    cpu.set_register('a', cpu.get_register('a') << 1)
    cpu.set_register('z', cpu.get_register('a'))
    cpu.set_register('n', cpu.get_register('a'))
def bcc(address):
    if cpu.get_register('c') == 0:
        blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int('0x' + str(address)[2:-1], base=0), 4, blazelib.libemu.current_console)
        cpu.branchcycles(int('0x' + str(address)[2:-1], base=0))
def bcs(address):
    if cpu.get_register('c') != 0:
        blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int('0x' + str(address)[2:-1], base=0), 4, blazelib.libemu.current_console)
        cpu.branchcycles(int('0x' + str(address)[2:-1], base=0))
def beq(address):
    if cpu.get_register('z') != 0:
        blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int('0x' + str(address)[2:-1], base=0), 4, blazelib.libemu.current_console)
        cpu.branchcycles(int('0x' + str(address)[2:-1], base=0))       
def bit(address):
    value = cpu.ram.read_8(int(b'0x' + address, base=0))
    cpu.set_register('v', (value >> 6) & 1)
    cpu.set_register('z', value & cpu.get_register('a'))
    cpu.set_register('n', value)
def bmi(address):
    if cpu.get_register('n') != 0:
        blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int('0x' + str(address)[2:-1], base=0), 4, blazelib.libemu.current_console)
        cpu.branchcycles(int('0x' + str(address)[2:-1], base=0))
def bne(address):
    if cpu.get_register('z') == 0:
        blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int('0x' + str(address)[2:-1], base=0), 4, blazelib.libemu.current_console)
        cpu.branchcycles(int('0x' + str(address)[2:-1], base=0))
def bpl(address):
    if cpu.get_register('n') == 0:
        blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int('0x' + str(address)[2:-1], base=0), 4, blazelib.libemu.current_console)
        cpu.branchcycles(int('0x' + str(address)[2:-1], base=0))
def bvc(address):
    if cpu.get_register('v') == 0:
        blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int('0x' + str(address)[2:-1], base=0), 4, blazelib.libemu.current_console)
        cpu.branchcycles(int('0x' + str(address)[2:-1], base=0))
def bvs(address):
    if cpu.get_register('v') != 0:
        blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int('0x' + str(address)[2:-1], base=0), 4, blazelib.libemu.current_console)
        cpu.branchcycles(int('0x' + str(address)[2:-1], base=0))
def inx(_):
    cpu.set_register('x', cpu.get_register('x') + 1)
    cpu.set_register('z', cpu.get_register('x'))
    cpu.set_register('n', cpu.get_register('x'))
def dex(_):
    cpu.set_register('x', cpu.get_register('x') - 1)
    cpu.set_register('z', cpu.get_register('x'))
    cpu.set_register('n', cpu.get_register('x'))
def iny(_):
    cpu.set_register('y', cpu.get_register('y') + 1)
    cpu.set_register('z', cpu.get_register('y'))
    cpu.set_register('n', cpu.get_register('y'))
def dey(_):
    cpu.set_register('x', cpu.get_register('y') - 1)
    cpu.set_register('z', cpu.get_register('x'))
    cpu.set_register('n', cpu.get_register('x'))

    
    
