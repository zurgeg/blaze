import blazelib.core
import blazelib.libemu
console = blazelib.core.load_console()
# NOTE: somerom.rom is a ROM of Techmo Super Bowl. Get it yourself because it's not here and we don't encourage piracy
blazelib.libemu.read_and_exec('somerom.rom', 20745, console)

