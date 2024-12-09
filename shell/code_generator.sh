#!/bin/bash

# Usage Check
if [ "$#" -ne 1 ]; then
    echo "Usage: ./code_generator.sh <source_file.litel>"
    exit 1
fi

INPUT_FILE=$1

# Step 1: Run Lexer
TOKENS=$(./shell/lexer.sh "$INPUT_FILE" 2>&1)
if [ $? -ne 0 ]; then
    >&2 echo "Error: Lexer command failed. Please check lexer.sh."
    exit 1
fi

if echo "$TOKENS" | grep -q "Lexical error"; then
    >&2 echo "Error: Lexical error detected. Aborting."
    exit 1
fi

if [ -z "$TOKENS" ]; then
    >&2 echo "Error: Lexer produced no output."
    exit 1
fi

# Step 2: Run Parser
AST=$(echo "$TOKENS" | ./shell/parser.sh 2>/dev/null)
if [ $? -ne 0 ] || [ -z "$AST" ]; then
    >&2 echo "Error: Parser failed to generate AST. Please check parser.sh."
    exit 1
fi

# Step 3: Generate C Code
CODE=$(echo "$AST" | python3 src/code_generator.py 2>&1)
if [ $? -ne 0 ]; then
    >&2 echo "Error: Code generation failed. Please check code_generator.py."
    exit 1
fi

# If everything succeeded, print only the generated C code
echo "$CODE"
