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
- **Literals** (Integer and String literals)
- **Word-based Operators**
- **Delimiters** (Parentheses, Braces, Semicolons)
- **Comments**

### 1.1. Keywords
- `make` - Used for variable declarations and assignments.
- `check` - Functions like a `for` or `while` loop condition.
- `shout` - Prints output to the console.
- `def` - Used to define a function.
- `if` - Used to define conditional logic.
- `else` - Provides an alternative block of code if the `if` condition fails.
- `return` - Returns a value from a function.
- `call` - Call and run the function

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
- **Addition Operator**: `add` -> Equivalent to `+`
- **Subtraction Operator**: `subtract` -> Equivalent to `-`
- **Multiplication Operator**: `multiply` -> Equivalent to `*`
- **Division Operator**: `divide` -> Equivalent to `/`

#### Comparison Operators:
- **Less than**: `less_than` -> Equivalent to `<`
- **Greater than**: `greater_than` -> Equivalent to `>`
- **Less than or equal to**: `less_equal` -> Equivalent to `<=`
- **Greater than or equal to**: `greater_equal` -> Equivalent to `>=`
- **Equal to**: `equal_to` -> Equivalent to `==`
- **Not equal to**: `not_equal_to` -> Equivalent to `!=`

#### Assignment Operator:
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


To run the lexer, change the current working directory to the root directory of the project.


Then, make sure to make `lexer.sh` script file executable by

`chmod +x ./shell/lexer.sh`


Then you can execute the lexer on files with `.litel` extension, and the result shall be output to your terminal. You can execute it by

`./shell/lexer.sh <source_file.litel>`


To output the result into a file, you can use `>` or  `>>` to redirect stdout by

`./shell/lexer.sh <source_file.litel> > <destination_file>`


Example `.litel` files and their expected outputs are located in the `./tests/sample_programs` directory.


## Parser

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
5. Assignment ::= Identifier 'assign' Expression
6. FunctionDef ::= 'def' Identifier '(' ParameterList ')' Block
7. ParameterList ::= ε  
   | Identifier  
   | Identifier ',' ParameterList
8. Block ::= '{' StatementList '}'
9. IfStatement ::= 'if' '(' Expression ')' Block ElseClause
10. ElseClause ::= ε  
    | 'else' Block
11. Loop ::= 'check' '(' Expression ')' Block
12. Output ::= 'shout' '(' Expression ')'
13. ReturnStatement ::= 'return' Expression
14. FunctionCallStatement ::= 'call' FunctionCall
15. Expression ::= RelationalExpression  
    | ListExpression
16. RelationalExpression ::= ArithmeticExpression RelationalExpression'
17. RelationalExpression' ::= ComparisonOperator ArithmeticExpression  
    | ε
18. ComparisonOperator ::= 'less_than'  
    | 'greater_than'  
    | 'less_equal'  
    | 'greater_equal'  
    | 'equal_to'  
    | 'not_equal_to'
19. ArithmeticExpression ::= Term ArithmeticExpression'
20. ArithmeticExpression' ::= AddOp Term ArithmeticExpression'  
    | ε
21. AddOp ::= 'add'  
    | 'subtract'
22. Term ::= Factor Term'
23. Term' ::= MulOp Factor Term'  
    | ε
24. MulOp ::= 'multiply' | 'divide'
25. Factor ::= 'subtract' Factor  
    | Primary
26. Primary ::= '(' Expression ')'  
    | Literal  
    | Identifier  
    | FunctionCall
27. FunctionCall ::= Identifier '(' ArgumentList ')'
28. ArgumentList ::= ε  
    | Expression  
    | Expression ',' ArgumentList
29. Literal ::= IntegerLiteral  
    | FloatLiteral  
    | StringLiteral
30. ListExpression ::= IntegerList  
    | FloatList  
    | StringList
31. IntegerList ::= '[' IntegerListElements ']'
32. IntegerListElements ::= IntegerLiteral IntegerListElements'  
    | ε
33. IntegerListElements' ::= ',' IntegerLiteral IntegerListElements'  
    | ε
34. FloatList ::= '[' FloatListElements ']'
35. FloatListElements ::= FloatLiteral FloatListElements'  
    | ε
36. FloatListElements' ::= ',' FloatLiteral FloatListElements'  
    | ε
37. StringList ::= '[' StringListElements ']'
38. StringListElements ::= StringLiteral StringListElements'  
    | ε
39. StringListElements' ::= ',' StringLiteral StringListElements'  
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
