def clear_screen():
    ...
def return_from_subroutine():
    ...
def exec_subroutine(arguments, instruction):
    if arguments == 'e0':
        clear_screen()
    if arguments == 'ee':
        return_from_subroutine()
    print(instruction[1])
    print(arguments)
    address = instruction[1] + str(arguments)[2:-1]
    print(f'Machine Language Subroutine {address}')
def jump_to(arguments, instruction):
    ...
        
        
