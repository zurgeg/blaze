mkdir bin
pip install nuitka
nuitka --standalone cli.py
move cli.dist/cli.exe cli.dist/blaze_cli.exe
powershell Compress-Archive cli.dist bin/win.zip
del cli.dist/*

