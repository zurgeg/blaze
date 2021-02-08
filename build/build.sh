#!/bin/sh
mkdir bin
pip3 install nuitka
python -m nuitka --standalone cli.py
python -m nuitka --standalone gui.py
mv cli.dist/cli cli.dist/blaze_cli
mv gui.dist/gui gui.dist/blaze_gui

