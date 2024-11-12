#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: shell/parser.sh <input_file.litel>"
    exit 1
fi

INPUT_FILE=$1

shell/lexer.sh "$INPUT_FILE" | python3 src/parser.py

