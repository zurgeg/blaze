mkdir bin
pip install nuitka
nuitka --standalone cli.py --assume-yes-for-downloads
nuitka --standalone gui.py --assume-yes-for-downloads
move cli.dist/cli.exe cli.dist/blaze_cli.exe
move gui.dist/gui.exe gui.dist/blaze_gui.exe
