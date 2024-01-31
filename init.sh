#!/bin/bash

VENV_DIR="venv"
KEY_FILE=".my.key"

if [ -d "$VENV_DIR" ]; then
    source venv/bin/activate
else
    python3 -m venv "$VENV_DIR"
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

if ! [ -e "$KEY_FILE" ]; then
    touch "$KEY_FILE"
    echo "created"
fi