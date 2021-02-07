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
        self.stall = 10
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
        return [self.a, self.x, self.y, self.c, self.z, self.i, self.b, self.n, self.v, self.n]
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
    def branchcycles(address):
        cpu.cycle()
        if blazelib.libemu.current_address&0xFF00 != address&0xFF00:
            cpu.cycle()
        
    
cpu = CPU()
class STPException(Exception):
    ...
def notbreak(*args):
    '''
    cpu.cycle()
    cpu.push_16(blazelib.libemu.current_addr)
    cpu.push(cpu.flags() | 0x10)
    cpu.set_register('i', 1)
    blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, 0xFFEE, 4, blazelib.libemu.current_console)
    '''
    print('break!'))
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
        blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int(str(address)[2:-1], base=8), 4, blazelib.libemu.current_console)
        cpu.branchcycles(address)
def bcs(address):
    if cpu.get_register('c') != 0:
        blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int(str(address)[2:-1], base=8), 4, blazelib.libemu.current_console)
        cpu.branchcycles(address)
def beq(address):
    if cpu.get_register('z') != 0:
        blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int(str(address)[2:-1], base=8), 4, blazelib.libemu.current_console)
        cpu.branchcycles(address)       
def bit(address):
    value = cpu.ram.read_8(int(b'0x' + address, base=0))
    cpu.set_register('v', (value >> 6) & 1)
    cpu.set_register('z', value & cpu.get_register('a'))
    cpu.set_register('n', value)
def bmi(address):
    if cpu.get_register('n') != 0:
        blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int(str(address)[2:-1], base=8), 4, blazelib.libemu.current_console)
        cpu.branchcycles(address)
def bne(address):
    if cpu.get_register('z') == 0:
        blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int(str(address)[2:-1], base=8), 4, blazelib.libemu.current_console)
        cpu.branchcycles(address)
def bpl(address):
    if cpu.get_register('n') == 0:
        blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int(str(address)[2:-1], base=8), 4, blazelib.libemu.current_console)
        cpu.branchcycles(address)
def bvc(address):
    if cpu.get_register('v') == 0:
        blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int(str(address)[2:-1], base=8), 4, blazelib.libemu.current_console)
        cpu.branchcycles(address)
def bvs(address):
    if cpu.get_register('v') != 0:
        blazelib.libemu.read_and_exec(blazelib.libemu.current_rom, int(str(address)[2:-1], base=8), 4, blazelib.libemu.current_console)
        cpu.branchcycles(address)

