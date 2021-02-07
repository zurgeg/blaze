mkdir bin
pip install nuitka
nuitka --standalone cli.py -o blaze_cli.exe
move cli.dist/* bin

