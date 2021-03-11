TYPE_GB = 0
TYPE_COLORGB = 1
TYPE_GBA = 2
TYPE_SUPERGB = 3
TYPE_SUPERGB2 = 4
TYPE_GBP = 5
TYPE_GBA_LIMITED = 0 # Standard GB mode on the GBA should have the same clock as a GB
REGION_US = 0
REGION_EU = 1
REGION_JP = 2
SECONDS_PER_HSYNC_NTSC = .000000485
SECONDS_PER_HSYNC_PAL = .00000047
import yaml
import base64
import blazelib.libemu
from time import sleep
def die(console, message):
    cpu = console.cpu
    print('ERROR')
    print('The emulation has crashed')
    print('If you ask for support, use this info')
    pc = blazelib.libemu.current_addr
    print(f'PC: {cpu.pc}')
    print(f'IE: {cpu.ie}')
    state = base64.b64encode(zlib.compress(base64.b64encode(bytes(cpu.console.dump(), encoding='utf-8'))))
    print(f'STATE: {state}')
    print(f'Error: {message}')
    exit() # Who knows what this will do
class IO:
    def __init__(self, controller, apu, display, cpu, linkcable):
        self.controller = controller
        self.apu = apu
        self.display = display
        self.cpu = cpu
    def read(self, address):
        if address == 0xFF00:
            return self.controller.read() # No clue if this is right
        elif address > 0xFF02:
            return self.linkcable.read(address - 0xFF01)
        elif address > 0xFF07:
            raise NotImplementedError
        elif address > 0xFF3F:
            return self.apu.read(address - 0xFF10)
        elif address > 0xFF4B:
            return self.display.read(address - 0xFF40)
        elif address > 0xFF70:
            raise NotImplementedError
        else:
            print('the emulator\'s probably gonna crash now\nhave fun!')

class Display:
    def __init__(self, vram):
        self.lcdc = 0
        self.stat = 0
        self.scy = 0
        self.ly = 0
        self.lyc = 0
        self.wy = 0
    def read(self, address):
        if address == 0xFF40:
            return self.lcdc
        elif address == 0xFF41:
            return self.stat
        elif address == 0xFF42:
            return self.scy
        elif address == 0xFF44:
            return self.ly
        elif address == 0xFF45:
            return self.lyc
        elif address == 0xFF4A:
            return self.wy
        else:
            return NotImplementedError


class APU:
    ...
class Controller:
    ...
class LinkCable:
    ...
class Cartridge:
    def __init__(self, file):
        self.file = file
        self.data = None
class Config:
    def __init__(self, console_type, region):
        self.console_type = console_type
        self.console_region = region
class Console(yaml.YAMLObject):
    def __init__(self, config, cpu, display, apu, cartridge, io, controller, linkcable):
        self.config = config
        self.cpu = cpu 
        self.display = display
        self.apu = apu
        self.cartridge = cartridge
        self.io = io
        self.controller = controller
        self.linkcable = linkcable
    def dump(self):
        return yaml.dump(self)
class MemoryMap:
    def __init__(self, console):
        self.config = console.config
        self.cpu = console.cpu
        self.display = console.display
        self.apu = console.apu
        self.cartridge = console.cartridge
        self.io = console.io
        self.console = console
    def read(self, address):
        rom = self.cartridge.data
        ram = self.cpu.ram
        display = self.display
        vram = self.cpu.vram
        if address < 0x3FFF:
            return rom[address]
        elif address < 0x7FFF:
            raise NotImplementedError
        elif address < 0x9FFF:
            return vram[address - 0x8000]
        elif address < 0xBFFF:
            raise NotImplementedError
        elif address < 0xCFFF:
            return ram[address - 0xC000]
        elif address < 0xDFFF:
            if self.config.console_type == TYPE_COLORGB:
                raise NotImplementedError
            else:
                return ram[address - 0xD000]
        elif address < 0xFDFF:
            return self.read(0xC000 + address - 0xE000) # I'm not even sure that's right
        elif address < 0xFE9F:
            return display.oamread(address - 0xFE00)
        elif address < 0xFEFF:
            print('Unusable RAM location.\nBut just because Nintendo says it\'s unusable, doesn\'t mean it is')
            return ram[address - 0xFEA0]
        elif address < 0xFF7F:
            return self.io.read(address)
        elif address < 0xFFFE:
            return ram[address - 0xFF80]
        elif address == 0xFFFF:
            return self.cpu.ie
        else:
            die(console, f'Unhandled read from {address}')

class CPU:
    def __init__(self, config):
        self.config = config
        self.af = 0
        self.bc = 0
        self.de = 0
        self.hl = 0
        self.sp = 0
        self.ram = [0]
        self.vram = [0]
        self.cycles = 0
        self.cycle_timer = 0
        self.seconds_per_cycle = .000000596
        if self.config.console_type == TYPE_GB or self.config.console_type == TYPE_GBP:
            self.clock = 4.194304 * 10000000
            self.ram = ram * 8000
            self.vram = vram * 8000
            self.vsync = 59.73
            self.hsync = 9198
        elif self.config.console_type == TYPE_COLORGB:
            self.clock = 8.388608 * 10000000
            self.ram = self.ram * 32000
            self.vram = self.vram * 16000
            self.vsync = 59.73
            self.hsync = 9198
        elif self.config.console_type == TYPE_SUPERGB or TYPE_SUPERGB2:
            self.clock = 4.295454 * 10000000
            self.ram = self.ram * 32000
            self.vram = self.vram * 16000
            self.vsync = 61.1679
            self.hsync = 9419.86
        elif self.config.console_type == TYPE_GBA:
            print('Why the heck are you trying to run Gameboy games at GBA speed')
            self.clock = 16.8 * 10000000
            self.ram = self.ram * 256000
            self.vram = self.vram * 16000
            self.vsync = 59.727500569606
            self.hsync = 9419.86
        else:
            raise Exception('Unknown console type, how the heck did you manage to do that?')
        self.apu = APU()
        self.controller = Controller()
        self.linkcable = LinkCable()
        self.display = Display(self.vram)
        self.cartridge = Cartridge(None)
        self.io = IO(self.controller, self.apu, self.display, self, self.linkcable)
        self.console = Console(self.config, self, self.display, self.apu, self.cartridge, self.io, self.controller, self.linkcable)
        self.ram_map = MemoryMap(self.console)
    def cycle(self, n_cycles):
        if self.cycle_timer >= 1:
            self.cycles = 0
            self.cycle_timer = 0
        if self.cycles >= self.clock:
            sleep((self.cycles - self.clock) * self.seconds_per_cycle)
            self.cycles = 0
            self.cycle_timer = 0
        else:
            self.cycles += n_cycles
            time_to_add = n_cycles * self.seconds_per_cycle
            sleep(time_to_add)
            self.cycle_timer += time_to_add
    def read(self, address):
        self.ram_map.read(address)
    def write(self, address, value):
        raise NotImplementedError

def nop(args):
    cpu.cycle(1)
def ld_bc(args):
    cpu.cycle(3)
    data = int(args, base=16)
    cpu.bc = data
def ld_bc_a(args):
    cpu.cycle(2)
    a = cpu.af & 0xFFFF0000
    addr = cpu.bc
    cpu.write(addr, a)
def inc_bc(args):
    cpu.cycle(2)
    cpu.bc += 1
def inc_b(args):
    pass
def dec_b(args):
    pass
def set_bit(v, index, x):
    """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
    mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
    v &= ~mask          # Clear the bit indicated by the mask (if x is False)
    if x:
        v |= mask         # If x was True, set the bit indicated by the mask.
    return v            # Return the result, we're done.
def rlca(args):
    cpu.cycle(1)
    a = cpu.af & 0xFFFF0000
    a <<= 1
    a_bit0 = a & 0b0000001
    a_bit1 = a & 0b0000010
    a_bit2 = a & 0b0000100
    a_bit3 = a & 0b0001000
    af = set_bit(cpu.af, 4, a_bit0)
    af = set_bit(af, 5, a_bit1)
    af = set_bit(af, 6, a_bit2)
    cpu.af = set_bit(af, 7, a_bit3)
def ld_a16_sp(args):
    cpu.cycle(5)
    data = int(args, base=16)
    cpu.write(data, sp & 0xFFFF0000)
    cpu.write(data + 1, sp & 0x0000FFFF)
def add_hl_bc(args):
    cpu.cycle(2)
    cpu.hl += cpu.bc
def ld_a_bc(args):
    cpu.cycle(2)
    a = cpu.read(cpu.bc)
    a_bit0 = a & 0b0000001
    a_bit1 = a & 0b0000010
    a_bit2 = a & 0b0000100
    a_bit3 = a & 0b0001000
    af = set_bit(cpu.af, 4, a_bit0)
    af = set_bit(af, 5, a_bit1)
    af = set_bit(af, 6, a_bit2)
    cpu.af = set_bit(af, 7, a_bit3)
def dec_bc(args):
    cpu.cycle(2)
    cpu.bc -= 1
config = Config(TYPE_SUPERGB2, REGION_JP)
cpu = CPU(config)











