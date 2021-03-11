from time import sleep
class GB:
    def __init__(self):
        self.af = 0x01B0
        self.bc = 0x0013
        self.de = 0x00D8
        self hl = 0x014D
        self.sp = 0xFFFE
        self.ram = [0] * 0xFFFF
    def cycle(self, n_cycles):
        sleep(0.001 * n_cycles * .4194304)


def nop(args):
    pass
def ldbc(args):
    pass
def ldbca(args):
    pass
def ldb(args):
    pass
def incbc(args):
    pass
def decbc(args):
    pass
def incb(args):
    pass
def decb(args):
    pass
def rlca(args):
    pass
def ld(args):
    pass
def addhl(args):
    pass
def lda(args):
    pass
def incc(args):
    pass
def decc(args):
    pass
def ldc(args):
    pass
def rrca(args):
    pass