import blazelib.core
import blazelib.libemu
console = blazelib.core.load_console()
blazelib.libemu.read_and_exec('somerom.rom', 20745, 2, console)


