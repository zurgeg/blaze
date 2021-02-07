#!/bin/sh
mkdir bin
pip3 install nuitka
python -m nuitka --standalone cli.py --output-dir bin -o blaze_cli
