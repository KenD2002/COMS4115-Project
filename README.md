# LiteLang

## Team Members
- **Cheng Yang** (UNI: cy2748)
- **Ken Deng** (UNI: kd3005)

## Introduction

LiteLang is a small and efficient general-purpose programming language designed with simplicity in mind. The goal of LiteLang is to offer a language with clear syntax and essential programming constructs, while translating the source code into C for performance optimization. 

The language supports basic features such as variables, conditional 'if' statements, looping constructs, and function definitions. We have implemented a lexer that tokenizes LiteLang source code, followed by a parser that transforms the tokens into an abstract syntax tree (AST). The final step involves translating the AST into C code, which can then be compiled for efficient execution.

LiteLang is designed to be both easy to learn and powerful, combining the readability of Python-like syntax with the performance of C.

---

## Lexical Grammar

### 1. Tokens

The following are the token types in this language:

- **Keywords**
- **Identifiers**
- **Literals** (Integer, Float, String, and List Literals)
- **Word-based Operators**
- **Delimiters** (Parentheses, Braces, Brackets, Semicolons, Commas)
- **Comments**

### 1.1. Keywords

- `make` - Used for variable declarations.
- `check` - Functions like a `while` loop condition.
- `shout` - Prints output to the console.
- `def` - Used to define a function.
- `if` - Used to define conditional logic.
- `else` - Provides an alternative block of code if the `if` condition fails.
- `return` - Returns a value from a function.
- `call` - Used to call a function.

### 1.2. Identifiers

- **Regular Expression**: `[a-zA-Z][a-zA-Z0-9_]*`
- **Examples**: `x`, `total_sum`, `myVariable`

### 1.3. Literals

#### Integer Literals

- **Regular Expression**: `[0-9]+`
- **Examples**: `0`, `11`, `414`

#### Float Literals

- **Regular Expression**: `[0-9]+\.[0-9]+`
- **Examples**: `3.14`, `0.001`, `123.456`

#### String Literals

- **Regular Expression**: `\"[^\"]*\"`
- **Examples**: `"Hello, World!"`, `"Sample string"`

#### List Literals

Lists are enclosed in square brackets `[` and `]` and contain a comma-separated list of expressions. All elements in a list must be of the same type (integers, floats, or strings).

- **Regular Expression**: `\[\]|\[(ELEM,)*ELEM\]`
- **Examples**:
  - `[1, 2, 3]` (Integer list)
  - `[1.1, 2.2, 3.3]` (Float list)
  - `["hello", "world"]` (String list)

### 1.4. Word-based Operators

The language uses word-based operators in the source code, which are internally mapped to their symbol equivalents during tokenization.

#### Arithmetic Operators

- **Addition Operator**: `add` -> Equivalent to `+`
- **Subtraction Operator**: `subtract` -> Equivalent to `-`
- **Multiplication Operator**: `multiply` -> Equivalent to `*`
- **Division Operator**: `divide` -> Equivalent to `/`

#### Comparison Operators

- **Less than**: `less_than` -> Equivalent to `<`
- **Greater than**: `greater_than` -> Equivalent to `>`
- **Less than or equal to**: `less_equal` -> Equivalent to `<=`
- **Greater than or equal to**: `greater_equal` -> Equivalent to `>=`
- **Equal to**: `equal_to` -> Equivalent to `==`
- **Not equal to**: `not_equal_to` -> Equivalent to `!=`

#### Assignment Operator

- **Assignment Operator**: `assign` -> Equivalent to `=`

### 1.5. Delimiters

- **LPAR**: `(` 
- **RPAR**: `)` 
- **LBRACE**: `{` 
- **RBRACE**: `}` 
- **LBRACKET**: `[` 
- **RBRACKET**: `]` 
- **SEMICOLON**: `;`
- **COMMA**: `,` 

### 2. Whitespace

- **WHITESPACE**: `\s+` (matches spaces, tabs, newlines, etc.)

### 3. Comments
- **COMMENT**: `//.*` matches any characters until the end of the line.
- Comments are ignored by the interpreter and are used to add notes or explanations to the source code.

---

## File Extension
LiteLang source files will use the `.litel` file extension to
differentiate the LiteLang code from other programming languages. 

---

## Installation and Execution

Before you can run LiteLang, make sure you have the following installed on your system:

1. **Python 3.x** (for running the LiteLang interpreter)

2. **GCC or Clang** (for compiling the generated C code)


To run the lexer or parser, change the current working directory to the root directory of the project.


Then, make sure to make `lexer.sh` and `parser.sh` script file executable by

`chmod +x ./shell/lexer.sh`
`chmod +x ./shell/parser.sh`


Then you can execute the lexer on files with `.litel` extension, and the result shall be output to your terminal. You can execute it by

`./shell/lexer.sh <source_file.litel>` or

`./shell/parser.sh <source_file.litel>`


To output the result into a file, you can use `>` or  `>>` to redirect stdout by

`./shell/lexer.sh <source_file.litel> > <destination_file>` or

`./shell/parser.sh <source_file.litel> > <destination_file>`




Example `.litel` files and their expected outputs are located in the `./tests/sample_programs` directory.


## Parser

This project uses Recursive Descent Parser.

### Context-Free Grammar (CFG)

1. Program ::= StatementList
2. StatementList ::= Statement  
   | Statement StatementList
3. Statement ::= VarDeclaration ';'
   | Assignment ';'
   | Output ';'
   | ReturnStatement ';'
   | FunctionCallStatement ';'
   | IfStatement
   | Loop
   | FunctionDef
   | ';'
4. VarDeclaration ::= 'make' Identifier 'assign' Expression
5. Assignable ::= Identifier
   | Identifier '[' Expression ']'
6. Assignment ::= Identifier 'assign' Expression
7. FunctionDef ::= 'def' Identifier '(' ParameterList ')' Block
8. ParameterList ::= ε  
   | Identifier  
   | Identifier ',' ParameterList
9. Block ::= '{' StatementList '}'
10. IfStatement ::= 'if' '(' Expression ')' Block ElseClause
11. ElseClause ::= ε  
    | 'else' Block
12. Loop ::= 'check' '(' Expression ')' Block
13. Output ::= 'shout' '(' Expression ')'
14. ReturnStatement ::= 'return' Expression
15. FunctionCallStatement ::= 'call' FunctionCall
16. Expression ::= RelationalExpression  
    | ListExpression
17. RelationalExpression ::= ArithmeticExpression RelationalExpression'
18. RelationalExpression' ::= ComparisonOperator ArithmeticExpression RelationalExpression'  
    | ε
19. ComparisonOperator ::= 'less_than'  
    | 'greater_than'  
    | 'less_equal'  
    | 'greater_equal'  
    | 'equal_to'  
    | 'not_equal_to'
20. ArithmeticExpression ::= Term ArithmeticExpression'
21. ArithmeticExpression' ::= AddOp Term ArithmeticExpression'  
    | ε
22. AddOp ::= 'add'  
    | 'subtract'
23. Term ::= Factor Term'
24. Term' ::= MulOp Factor Term'  
    | ε
25. MulOp ::= 'multiply' 
    | 'divide'
26. Factor ::= 'call' FunctionCall
    | '-' Factor
    | Primary
27. Primary ::= '(' Expression ')'
    | Literal
    | Identifier
    | Identifier '[' Expression ']'
    | FunctionCall
28. FunctionCall ::= Identifier '(' ArgumentList ')'
29. ArgumentList ::= ε  
    | Expression  
    | Expression ',' ArgumentList
30. Literal ::= IntegerLiteral  
    | FloatLiteral  
    | StringLiteral
31. ListExpression ::= IntegerList  
    | FloatList  
    | StringList
32. IntegerList ::= '[' IntegerListElements ']'
33. IntegerListElements ::= IntegerLiteral IntegerListElements'  
    | ε
34. IntegerListElements' ::= ',' IntegerLiteral IntegerListElements'  
    | ε
35. FloatList ::= '[' FloatListElements ']'
36. FloatListElements ::= FloatLiteral FloatListElements'  
    | ε
37. FloatListElements' ::= ',' FloatLiteral FloatListElements'  
    | ε
38. StringList ::= '[' StringListElements ']'
39. StringListElements ::= StringLiteral StringListElements'  
    | ε
40. StringListElements' ::= ',' StringLiteral StringListElements'  
    | ε

### Non-Terminals and Terminals

#### Non-Terminals

- **Program**
- **StatementList**
- **Statement**
- **VarDeclaration**
- **Assignment**
- **FunctionDef**
- **IfStatement**
- **ElseClause**
- **Loop**
- **Output**
- **ReturnStatement**
- **FunctionCallStatement**
- **Expression**
- **RelationalExpression**
- **RelationalExpression'**
- **ArithmeticExpression**
- **ArithmeticExpression'**
- **Term**
- **Term'**
- **Factor**
- **Primary**
- **FunctionCall**
- **ArgumentList**
- **ParameterList**
- **Block**
- **Literal**
- **ListExpression**
- **IntegerList**
- **FloatList**
- **StringList**
- **IntegerListElements**
- **IntegerListElements'**
- **FloatListElements**
- **FloatListElements'**
- **StringListElements**
- **StringListElements'**

#### Terminals

- **Keywords**: `'make'`, `'assign'`, `'def'`, `'if'`, `'else'`, `'check'`, `'shout'`, `'return'`, `'call'`
- **Arithmetic Operators**: `'add'`, `'subtract'`, `'multiply'`, `'divide'`
- **Comparison Operators**: `'less_than'`, `'greater_than'`, `'less_equal'`, `'greater_equal'`, `'equal_to'`, `'not_equal_to'`
- **Delimiters**: `'('`, `')'`, `'{'`, `'}'`, `'['`, `']'`, `','`, `';'`
- **Identifier**
- **IntegerLiteral**
- **FloatLiteral**
- **StringLiteral**
