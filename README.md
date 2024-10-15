# COMS4156-Project
# Tiny General-Purpose Programming Language Interpreter

## Team Members
- **Cheng Yang** (UNI: cy2748)
- **Ken Deng** (UNI: kd3005)

## Introduction
Our project focuses on creating a tiny general-purpose programming language interpreter. The goal is to design a simple but functional programming language with key features such as variables, conditional 'if' statements, and looping constructs. We are using Python to write the lexer and parser, which will translate our language into C, allowing for efficient execution. The project will involve designing the syntax and grammar of the language, ensuring it can handle basic programming constructs. We will implement a lexer that breaks down the source code into tokens, followed by a parser that will convert these tokens into a structured format that can be interpreted. Then, we'll build the interpreter, which will execute the parsed code. By the end of the project, we aim to have a fully functional interpreter that can take in programs written in our new language and convert them to C, where they can be compiled.

---

## Lexical Grammar

### 1. Tokens
The following are the token types in this language:

- **Keywords**
- **Identifiers**
- **Literals** (Integer and String literals)
- **Word-based Operators**
- **Delimiters** (Parentheses, Braces, Semicolons)

### 1.1. Keywords
- `make` - Used for variable declarations and assignments.
- `check` - Functions like a `for` or `while` loop condition.
- `shout` - Prints output to the console.
- `def` - Used to define a function.
- `if` - Used to define conditional logic.
- `else` - Provides an alternative block of code if the `if` condition fails.
- `return` - Returns a value from a function.

### 1.2. Identifiers
- Regular Expression: `[a-zA-Z][a-zA-Z0-9]*`
- **Examples**: `x`, `total_sum`

### 1.3. Literals
#### Integer Literal:
- Regular Expression: `[0-9]+`
- **Examples**: `0`, `11`, `414`

#### String Literal:
- Regular Expression: `\"[^\"]*\"`
- **Examples**: `"Hello, World!"`

### 1.4. Word-based Operators
#### Arithmetic Operators:
- **Addition Operator**: `add` → Equivalent to `+`
- **Subtraction Operator**: `subtract` → Equivalent to `-`
- **Multiplication Operator**: `multiply` → Equivalent to `*`
- **Division Operator**: `divide` → Equivalent to `/`

#### Comparison Operators:
- **Less than**: `less_than` → Equivalent to `<`
- **Greater than**: `greater_than` → Equivalent to `>`
- **Less than or equal to**: `less_equal` → Equivalent to `<=`
- **Greater than or equal to**: `greater_equal` → Equivalent to `>=`
- **Equal to**: `equal_to` → Equivalent to `==`
- **Not equal to**: `not_equal_to` → Equivalent to `!=`

#### Assignment Operator:
- **Assignment Operator**: `assign` → Equivalent to `=`

### 1.5. Delimiters
- **LPAR**: `(` 
- **RPAR**: `)` 
- **LBRACE**: `{` 
- **RBRACE**: `}` 
- **SEMICOLON**: `;`
- **COMMA**: `,` 

---

### 2. Whitespace
- **WHITESPACE**: `\s+` (matches spaces, tabs, newlines, etc.)

---

### 3. Comments
- **COMMENT**: `//.*` (matches single-line comments)
- **Example**: `// This is a comment`
