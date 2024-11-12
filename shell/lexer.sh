#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: ./lexer.sh <source_file>"
  exit 1
fi

python3 src/scanner.py "$1"