#!/bin/sh
mkdir bin
pip3 install nuitka
python -m nuitka --standalone cli.py -o blaze_cli
mv cli.dist/* bin
