#!/bin/bash

# Check if input is provided via a file or piped input
if [ -p /dev/stdin ]; then
    # If tokens are piped in directly
    TOKENS=$(cat)
else
    if [ "$#" -ne 1 ]; then
        echo "Usage: ./shell/parser.sh <input_file.litel>"
        exit 1
    fi
    # Run the lexer on the provided file
    TOKENS=$(./shell/lexer.sh "$1" 2>&1)
fi

# Check for lexical errors
if echo "$TOKENS" | grep -q "Lexical error"; then
    echo "Error: Lexical analysis failed. Invalid token."
    exit 1
fi

# If no lexical error, pipe tokens into the parser
echo "$TOKENS" | python3 src/parser.py
