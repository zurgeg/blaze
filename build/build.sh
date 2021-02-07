#!/bin/sh
mkdir bin
pip3 install nuitka
python -m nuitka --standalone cli.py
mv cli.dist/cli cli.dist/blaze_cli
zip -r cli.dist.zip cli.dist
mv cli.dist.zip bin/linux_nightly.zip
rm -rf cli.dist/
