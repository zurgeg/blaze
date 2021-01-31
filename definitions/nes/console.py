class STPException():
    ...
def notbreak(_):
    print('break!')
def ora(_):
    print('ORA instruction')
def stp(_):
    print('STP instruction. Stop maybe?')
    raise STPException('Encountered a stop instruction, halt')
