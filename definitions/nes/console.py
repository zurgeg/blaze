class STPException():
    ...
def notbreak():
    print('break!')
def ora():
    print('ORA instruction')
def stp():
    print('STP instruction. Stop maybe?')
    raise STPException('Encountered a stop instruction, halt')
