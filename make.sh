#!bin/bash

mkdir rain
cp LICENSE.txt rain/LICENSE.txt
cp README.md rain/README.md
pyinstaller --onefile --distpath rain rain.py
zip -r rain.zip rain
rm -rf rain