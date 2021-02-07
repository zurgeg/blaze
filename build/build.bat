mkdir bin
pip install nuitka
nuitka --standalone cli.py --output-dir bin -o blaze_cli.exe
