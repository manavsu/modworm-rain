#!bin/bash

mkdir rain
cp LICENSE.txt rain/LICENSE.txt
cp README.md rain/README.md
pyinstaller --onefile --distpath rain rain.py

if [[ "$(uname)" == "Darwin" ]]; then
    zip -r rain.zip rain
elif [[ "$(uname)" =~ MINGW ]]; then
    Compress-Archive -Path rain/* -DestinationPath rain.zip
else
    echo "Unknown operating system, unable to zip the folder."
fi

rm -rf rain