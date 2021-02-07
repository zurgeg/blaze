mkdir bin
pip install nuitka
nuitka --standalone cli.py --assume-yes-for-downloads
move cli.dist/cli.exe cli.dist/blaze_cli.exe
powershell Compress-Archive cli.dist bin/windows_nightly.zip
del cli.dist/*

