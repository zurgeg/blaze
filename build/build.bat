mkdir bin
pip install nuitka
nuitka --standalone cli.py --assume-yes-for-downloads
move cli.dist/cli.exe cli.dist/blaze_cli.exe
tar.exe -a -c -f bin/windows_nightly.zip cli.dist
del cli.dist/*

