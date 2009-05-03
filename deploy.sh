#!/bin/bash

python setup.py bdist_egg
cp dist/Strac-0.1-py2.5.egg /home/smash/src/tracbox/plugins/
clear

echo "Starting Trac on port 3000..."

tracd --port 3000 /home/smash/src/tracbox
