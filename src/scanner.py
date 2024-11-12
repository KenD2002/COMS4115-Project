import sys

class Scanner:
    def __init__(self):
        self.state = 'START'
        self.tokens = []
        self.current_char = ''

    def scan(self, code):
        i = 0
        start = 0
        self.state = 'START'
        self.tokens = []
        self.current_char = ''
        keywords = {
            "make", 
            "check", 
            "shout", 
            "if", 
            "else", 
            "return",
            "def",
            "call"
        }
        operators = {
            "add": "+",
            "subtract": "-",
            "multiply": "*",
            "divide": "/",
            "less_than": "<",
            "greater_than": ">",
            "less_equal": "<=",
            "greater_equal": ">=", 
            "equal_to": "==",
            "not_equal_to": "!=",
            "assign": "="
        }


        while i < len(code):
            self.current_char = code[i]

            # DFA State Transitions
            if self.state == 'START':
                # Skip whitespace
                if self.current_char.isspace():
                    i += 1  
                # Goes to COMMENT state
                # Skip the input after '//' until the end of line
                elif self.current_char == '/' and i + 1 < len(code) and code[i + 1] == '/':
                    self.state = 'COMMENT'
                    i += 2  
                # Goes to IDENTIFIER state
                # Matches identifier, keyword, or operator starts with a letter
                elif self.current_char.isalpha():  
                    self.state = 'IDENTIFIER'
                    start = i  # Mark start of identifier or keyword
                    i += 1
                # Goes to NUMBER state
                # Matches any number starts with a digit
                elif self.current_char.isdigit():  
                    self.state = 'NUMBER'
                    start = i  # Mark start of number
                    i += 1
                # Goes to STRING state
                # Matches String literal starts and ends with "
                elif self.current_char == '"':  
                    self.state = 'STRING'
                    start = i  # Mark start of string
                    i += 1
                # Add LPAR to tokens list
                elif self.current_char == '(':
                    self.tokens.append(('LPAR', '('))
                    i += 1
                # Add RPAR to tokens list
                elif self.current_char == ')':
                    self.tokens.append(('RPAR', ')'))
                    i += 1
                # Add LBRACKET to token list
                elif self.current_char == '[': 
                    self.tokens.append(('LBRACKET', '['))
                    i += 1
                # Add RBRACKET to token list
                elif self.current_char == ']': 
                    self.tokens.append(('RBRACKET', ']'))
                    i += 1
                # Add COMMA to tokens list
                elif self.current_char == ',':
                    self.tokens.append(('COMMA', ','))
                    i += 1
                # Add LBRACE to tokens list
                elif self.current_char == '{':
                    self.tokens.append(('LBRACE', '{'))
                    i += 1
                # Add RBRACE to tokens list
                elif self.current_char == '}':
                    self.tokens.append(('RBRACE', '}'))
                    i += 1
                # Add SEMICOLON to tokens list
                elif self.current_char == ';':
                    self.tokens.append(('SEMICOLON', ';'))
                    i += 1
                # Scanned unexpected character
                else:
                    print(f"Lexical error: Unexpected character '{self.current_char}' at position {i}")
                    return
                
            # State for handling comments
            elif self.state == 'COMMENT':
                if self.current_char == '\n':  # End of the comment line
                    self.state = 'START'
                i += 1  # Skip the rest of the line

            # State for handling identifiers, operators, or keywords
            elif self.state == 'IDENTIFIER':
                if self.current_char.isalnum() or self.current_char == '_':
                    i += 1  # Continue reading identifier
                else:
                    identifier = code[start:i]
                    if identifier in keywords:
                        self.tokens.append(('KEYWORD', identifier))
                    elif identifier in operators:
                        self.tokens.append(('OPERATOR', operators[identifier]))
                    else:
                        self.tokens.append(('IDENTIFIER', identifier))
                    self.state = 'START'  # Reinitialize state
                    start = i  # Reset start for the next token

            # State for handling numbers
            elif self.state == 'NUMBER':
                if self.current_char.isdigit():
                    i += 1  # Continue reading number
                elif self.current_char == '.' and (i + 1) < len(code) and code[i + 1].isdigit():
                    # Check if it's a float by seeing if a digit follows the decimal point
                    self.state = 'FLOAT'
                    i += 1
                elif self.current_char.isalpha():  # Error: numbers followed by letters
                    print(f"Lexical error: Invalid token starting with a number at position {start}.")
                    return
                else:
                    # If we don't encounter a '.', this is an integer
                    number = code[start:i]
                    self.tokens.append(('INTLITERAL', number))
                    self.state = 'START'
                    start = i

            # State for handling floats
            elif self.state == 'FLOAT':
                if self.current_char.isdigit():
                    i += 1
                elif self.current_char == '.':
                    # If a number has more than one decimal point
                    print(f"Lexical error: Invalid float format with multiple decimal points at position {i}.")
                    return
                elif self.current_char.isalpha():  # Error: numbers followed by letters
                    print(f"Lexical error: Invalid token starting with a number at position {start}.")
                    return
                else:
                    # Read complete
                    float_number = code[start:i]
                    self.tokens.append(('FLOATLITERAL', float_number))
                    self.state = 'START'
                    start = i

            # State for handling string literals
            elif self.state == 'STRING':
                if self.current_char == '"':  # Closing quote
                    string_literal = code[start:i+1]
                    self.tokens.append(('STRINGLITERAL', string_literal))
                    self.state = 'START'  # Reinitialize state
                    i += 1  # Move past the closing quote
                    start = i  # Reset start for the next token
                elif i == len(code) - 1:  # If the string reaches the end without closing
                    print(f"Lexical error: Unterminated string literal at position {start}.")
                    return
                else:
                    i += 1  # Continue reading string literal

        return self.tokens
    


def read_input_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found. Please check the file path.")
        sys.exit(1)
    except IOError as e:
        print(f"Error: An error occurred while reading the file: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scanner.py <input_file.lang>")
        print("Please provide exactly one input file for the scanner.")
        sys.exit(1)

    input_file = sys.argv[1]

    code = read_input_file(input_file)

    # Append a whitespace to the end of the code to ensure proper token detection
    code += ' '

    scanner = Scanner()
    tokens = scanner.scan(code)

    if tokens:
        for token in tokens:
            print(f"<{token[0]}, {token[1]}>")

if __name__ == "__main__":
    main()
