import sys
import re

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def match(self, expected_type, expected_value=None):
        token = self.current_token()
        if (token and token[0] == expected_type) and ((expected_value is None) or (token[1] == expected_value)):
            self.pos += 1
            return token
        else:
            expected = f"{expected_type} '{expected_value}'" if expected_value else expected_type
            actual = f"{token[0]} '{token[1]}'" if token else "EOF"
            raise SyntaxError(f"Expected {expected}, but found {actual}")

    def parse(self):
        return self.parse_program()

    def parse_program(self):
        statements = []
        while self.current_token():
            statements.append(self.parse_statement())
        return {"Program": statements}

    def parse_statement(self):
        token = self.current_token()
        if token[0] == "KEYWORD":
            if token[1] == "make":
                return self.parse_var_declaration()
            elif token[1] == "shout":
                return self.parse_output()
            elif token[1] == "return":
                return self.parse_return_statement()
            elif token[1] == "call":
                return self.parse_function_call_statement()
            elif token[1] == "if":
                return self.parse_if_statement()
            elif token[1] == "check":
                return self.parse_loop()
            elif token[1] == "def":
                return self.parse_function_def()
            elif token[1] == ";":
                self.match("KEYWORD", ";")
                return {"EmptyStatement": ";"}
            else:
                raise SyntaxError(f"Unexpected keyword: {token[1]}")
        elif token[0] == "IDENTIFIER":
            # Could be an assignment or an expression
            next_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if next_token and (next_token[0] == "OPERATOR" and next_token[1] == "=") or next_token[0] == "LBRACKET":
                return self.parse_assignment()
            else:
                raise SyntaxError(f"Unexpected token after identifier: {next_token}")
        elif token[0] == "SEMICOLON":
            self.match("SEMICOLON")
            return {"EmptyStatement": ";"}
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def parse_var_declaration(self):
        self.match("KEYWORD", "make")
        identifier = self.match("IDENTIFIER")
        self.match("OPERATOR", "=")
        expr = self.parse_expression()
        self.match("SEMICOLON")
        return {"VarDeclaration": {"Identifier": identifier[1], "Expression": expr}}

    def parse_assignment(self):
        assignable = self.parse_assignable()
        self.match("OPERATOR", "=")
        expr = self.parse_expression()
        self.match("SEMICOLON")
        return {"Assignment": {"Assignable": assignable, "Expression": expr}}

    def parse_assignable(self):
        # Parse an Assignable: Identifier or Identifier '[' Expression ']'
        identifier = self.match("IDENTIFIER")[1]
        if self.current_token() and self.current_token()[0] == "LBRACKET":
            self.match("LBRACKET")
            index_expr = self.parse_expression()
            self.match("RBRACKET")
            return {"IndexedIdentifier": {"Identifier": identifier, "Index": index_expr}}
        else:
            return {"Identifier": identifier}

    def parse_output(self):
        self.match("KEYWORD", "shout")
        self.match("LPAR")
        expr = self.parse_expression()
        self.match("RPAR")
        self.match("SEMICOLON")
        return {"Output": expr}

    def parse_return_statement(self):
        self.match("KEYWORD", "return")
        expr = self.parse_expression()
        self.match("SEMICOLON")
        return {"Return": expr}

    def parse_function_call_statement(self):
        self.match("KEYWORD", "call")
        func_call = self.parse_function_call()
        self.match("SEMICOLON")
        return {"FunctionCallStatement": func_call}

    def parse_if_statement(self):
        self.match("KEYWORD", "if")
        self.match("LPAR")
        condition = self.parse_expression()
        self.match("RPAR")
        then_block = self.parse_block()
        else_block = None
        if self.current_token() and self.current_token()[0] == "KEYWORD" and self.current_token()[1] == "else":
            self.match("KEYWORD", "else")
            else_block = self.parse_block()
        return {"IfStatement": {"Condition": condition, "Then": then_block, "Else": else_block}}

    def parse_loop(self):
        self.match("KEYWORD", "check")
        self.match("LPAR")
        condition = self.parse_expression()
        self.match("RPAR")
        block = self.parse_block()
        return {"Loop": {"Condition": condition, "Block": block}}

    def parse_function_def(self):
        self.match("KEYWORD", "def")
        func_name = self.match("IDENTIFIER")
        self.match("LPAR")
        parameters = self.parse_parameter_list()
        self.match("RPAR")
        body = self.parse_block()
        return {"FunctionDef": {"Name": func_name[1], "Parameters": parameters, "Body": body}}

    def parse_parameter_list(self):
        params = []
        if self.current_token() and self.current_token()[0] == "IDENTIFIER":
            params.append(self.match("IDENTIFIER")[1])
            while self.current_token() and self.current_token()[0] == "COMMA":
                self.match("COMMA")
                params.append(self.match("IDENTIFIER")[1])
        return params

    def parse_block(self):
        self.match("LBRACE")
        statements = []
        while self.current_token() and self.current_token()[0] != "RBRACE":
            statements.append(self.parse_statement())
        self.match("RBRACE")
        return {"Block": statements}

    def parse_expression(self):
        if self.current_token()[0] == "LBRACKET":
            return self.parse_list_expression()
        else:
            return self.parse_relational_expression()

    def parse_relational_expression(self):
        left = self.parse_arithmetic_expression()
        while self.current_token() and self.current_token()[0] == "OPERATOR" and self.current_token()[1] in ["<", ">", "<=", ">=", "==", "!="]:
            operator = self.match("OPERATOR")
            right = self.parse_arithmetic_expression()
            left = {"RelationalExpression": {"Left": left, "Operator": operator[1], "Right": right}}
        return left

    def parse_arithmetic_expression(self):
        left = self.parse_term()
        while self.current_token() and self.current_token()[0] == "OPERATOR" and self.current_token()[1] in ["+", "-"]:
            operator = self.match("OPERATOR")
            right = self.parse_term()
            left = {"ArithmeticExpression": {"Left": left, "Operator": operator[1], "Right": right}}
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token() and self.current_token()[0] == "OPERATOR" and self.current_token()[1] in ["*", "/"]:
            operator = self.match("OPERATOR")
            right = self.parse_factor()
            left = {"Term": {"Left": left, "Operator": operator[1], "Right": right}}
        return left

    def parse_factor(self):
        token = self.current_token()
        if token[0] == "KEYWORD" and token[1] == "call":
            self.match("KEYWORD", "call")
            func_call = self.parse_function_call()
            return {"FunctionCall": func_call}
        elif token[0] == "OPERATOR" and token[1] == "-":
            self.match("OPERATOR", "-")
            factor = self.parse_factor()
            return {"UnaryExpression": {"Operator": "-", "Operand": factor}}
        else:
            return self.parse_primary()

    def parse_primary(self):
        token = self.current_token()
        if token[0] == "INTLITERAL":
            value = int(self.match("INTLITERAL")[1])
            return {"IntegerLiteral": value}
        elif token[0] == "FLOATLITERAL":
            value = float(self.match("FLOATLITERAL")[1])
            return {"FloatLiteral": value}
        elif token[0] == "STRINGLITERAL":
            value = self.match("STRINGLITERAL")[1]
            return {"StringLiteral": value}
        elif token[0] == "IDENTIFIER":
            identifier = self.match("IDENTIFIER")[1]
            # Check for list indexing
            if self.current_token() and self.current_token()[0] == "LBRACKET":
                self.match("LBRACKET")
                index_expr = self.parse_expression()
                self.match("RBRACKET")
                return {"IndexedIdentifier": {"Identifier": identifier, "Index": index_expr}}
            # Check if it's a function call without 'call'
            elif self.current_token() and self.current_token()[0] == "LPAR":
                func_call = self.parse_function_call(identifier)
                return {"FunctionCall": func_call}
            else:
                return {"Identifier": identifier}
        elif token[0] == "LPAR":
            self.match("LPAR")
            expr = self.parse_expression()
            self.match("RPAR")
            return expr
        elif token[0] == "LBRACKET":
            # Handle list literals
            return self.parse_list_expression()
        else:
            raise SyntaxError(f"Unexpected token in primary: {token}")

    def parse_function_call(self, func_name=None):
        if not func_name:
            func_name = self.match("IDENTIFIER")[1]
        self.match("LPAR")
        args = self.parse_argument_list()
        self.match("RPAR")
        return {"Name": func_name, "Arguments": args}

    def parse_argument_list(self):
        args = []
        if self.current_token() and self.current_token()[0] != "RPAR":
            args.append(self.parse_expression())
            while self.current_token() and self.current_token()[0] == "COMMA":
                self.match("COMMA")
                args.append(self.parse_expression())
        return args

    def parse_list_expression(self):
        token = self.current_token()
        if token[0] == "LBRACKET":
            self.match("LBRACKET")
            elements, element_type = self.parse_list_elements()
            self.match("RBRACKET")
            return {"ListExpression": {"Type": element_type, "Elements": elements}}
        else:
            raise SyntaxError(f"Expected '[' to start a list, but found: {token}")

    def parse_list_elements(self):
        elements = []
        element_type = None
        # Handle empty list
        if self.current_token() and self.current_token()[0] == "RBRACKET":
            return elements, element_type
        else:
            # Parse first element
            first_element = self.parse_expression()
            element_type = self.get_expression_type(first_element)
            elements.append(first_element)
            while self.current_token() and self.current_token()[0] == "COMMA":
                self.match("COMMA")
                next_element = self.parse_expression()
                next_element_type = self.get_expression_type(next_element)
                if next_element_type != element_type:
                    raise SyntaxError(f"Type mismatch in list elements: Expected {element_type}, found {next_element_type}")
                elements.append(next_element)
            return elements, element_type

    def get_expression_type(self, expr):
        if isinstance(expr, dict):
            if "IntegerLiteral" in expr:
                return "int"
            elif "FloatLiteral" in expr:
                return "float"
            elif "StringLiteral" in expr:
                return "string"
            elif "Identifier" in expr:
                # For simplicity, we assume identifiers have the same type as their first occurrence
                return "identifier"
            elif "IndexedIdentifier" in expr:
                # Assume the type is the same as the base identifier
                return "identifier"
            elif "FunctionCall" in expr:
                # Return type unknown at parse time; for now, accept
                return "unknown"
            else:
                # For other expressions, recursively check their sub-expressions
                for key in expr:
                    return self.get_expression_type(expr[key])
        else:
            return "unknown"

    def format_ast(self, node, prefix="", is_root=True):
        if isinstance(node, dict):
            for i, (key, value) in enumerate(node.items()):
                is_last = i == len(node) - 1
                if is_root:
                    print(f"{key}")
                    self.format_ast(value, prefix, is_root=False)
                else:
                    print(f"{prefix}{'└── ' if is_last else '├── '}{key}")
                    self.format_ast(value, prefix + ("    " if is_last else "│   "), is_root=False)
        elif isinstance(node, list):
            for i, item in enumerate(node):
                is_last = i == len(node) - 1
                print(f"{prefix}{'└── ' if is_last else '├── '}{'List Item'}")
                self.format_ast(item, prefix + ("    " if is_last else "│   "), is_root=False)
        else:
            print(f"{prefix}{'└── '}{node}")

def main():
    tokens = []
    for line in sys.stdin:
        match = re.match(r"<([^,]+),\s*(.+)>", line.strip())
        if match:
            token_type = match.group(1)
            token_value = match.group(2).strip()
            tokens.append((token_type, token_value))
        else:
            print("Error: Incorrect token format in tokens input.")
            sys.exit(1)

    parser = Parser(tokens)
    try:
        ast = parser.parse()
        print("Formatted AST:")
        parser.format_ast(ast)
        print("\n\nAST:")
        print(ast)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")

if __name__ == "__main__":
    main()
