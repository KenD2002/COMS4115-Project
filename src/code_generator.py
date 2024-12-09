import sys
import json

class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.main_code = ""
        self.functions_code = ""
        self.indent_level = 1
        self.variables = {}
        self.function_return_type = {}
        self.in_function_definition = False
        self.current_function_return_type = None

    def indent(self):
        return "    " * self.indent_level

    def generate_code(self):
        if "Program" not in self.ast:
            raise Exception("AST does not have a Program node.")
        program_body = self.ast["Program"]

        for stmt in program_body:
            self.visit(stmt, in_main=True)

        c_code = "#include <stdio.h>\n#include <string.h>\n\n"
        c_code += self.functions_code
        c_code += "int main() {\n"
        c_code += self.main_code
        c_code += "    return 0;\n}\n"
        return c_code

    def visit(self, node, in_main=False):
        if not isinstance(node, dict):
            raise Exception(f"Node is not a dict: {node}")
        if len(node.keys()) != 1:
            raise Exception(f"Node has multiple keys: {node.keys()}")

        node_type = list(node.keys())[0]
        node_value = node[node_type]
        method_name = f"visit_{node_type}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node_value, in_main)

    def generic_visit(self, node_value, in_main):
        raise Exception(f"No visitor method defined for this node type or unexpected node: {node_value}")

    def visit_VarDeclaration(self, node, in_main):
        identifier = node["Identifier"]
        expr = node["Expression"]
        expr_code, expr_type = self.generate_expression(expr)

        if isinstance(expr_code, list):
            # Arrays
            base_type = expr_type.replace("[]", "")
            line = f"{base_type} {identifier}[] = {{{', '.join(expr_code)}}};\n"
            self.variables[identifier] = base_type
        else:
            c_type = self.map_type(expr_type)
            line = f"{c_type} {identifier} = {expr_code};\n"
            self.variables[identifier] = c_type

        self.append_code(line, in_main)

    def visit_Assignment(self, node, in_main):
        assignable = node["Assignable"]
        expr = node["Expression"]
        expr_code, expr_type = self.generate_expression(expr)

        if "Identifier" in assignable:
            var_name = assignable["Identifier"]
            line = f"{var_name} = {expr_code};\n"
        elif "IndexedIdentifier" in assignable:
            var_name = assignable["IndexedIdentifier"]["Identifier"]
            index_expr = assignable["IndexedIdentifier"]["Index"]
            index_code, _ = self.generate_expression(index_expr)
            line = f"{var_name}[{index_code}] = {expr_code};\n"
        else:
            raise Exception("Unknown assignable node")

        self.append_code(line, in_main)

    def visit_Output(self, node, in_main):
        expr = node
        expr_code, expr_type = self.generate_expression(expr)
        if expr_type == "int":
            line = f'printf("%d\\n", {expr_code});\n'
        elif expr_type == "float":
            line = f'printf("%f\\n", {expr_code});\n'
        elif expr_type == "string":
            line = f'printf("%s\\n", {expr_code});\n'
        else:
            line = f'printf("%s\\n", {expr_code});\n'
        self.append_code(line, in_main)

    def visit_Return(self, node, in_main):
        expr = node
        expr_code, expr_type = self.generate_expression(expr)
        if self.in_function_definition:
            if self.current_function_return_type is None:
                self.current_function_return_type = expr_type
            else:
                if self.current_function_return_type != expr_type:
                    raise Exception("Error: Multiple return types in function body are not consistent.")
            if "[]" in self.current_function_return_type:
                raise Exception("Error: Returning arrays is not allowed.")

        line = f"return {expr_code};\n"
        self.append_code(line, in_main)

    def visit_FunctionCallStatement(self, node, in_main):
        func_call = node
        func_name = func_call["Name"]
        args = func_call["Arguments"]
        args_code = []
        for arg in args:
            arg_code, _ = self.generate_expression(arg)
            args_code.append(arg_code)
        line = f"{func_name}({', '.join(args_code)});\n"
        self.append_code(line, in_main)

    def visit_IfStatement(self, node, in_main):
        condition = node["Condition"]
        then_block = node["Then"]
        else_block = node["Else"]

        # Attempt to evaluate condition at compile time if possible
        cond_decision = self.evaluate_condition_if_purely_numeric(condition)
        # cond_decision can be True, False, or None (if uncertain)

        if cond_decision is True:
            # Condition always true -> generate only then_block
            for stmt in then_block["Block"]:
                self.visit(stmt, in_main)
        elif cond_decision is False:
            # Condition always false -> generate else_block if exists
            if else_block is not None:
                for stmt in else_block["Block"]:
                    self.visit(stmt, in_main)
            # else no code generated
        else:
            # Unknown condition, generate normal if-else
            cond_code, _ = self.generate_expression(condition)
            line = f"if ({cond_code}) {{\n"
            self.append_code(line, in_main)
            self.indent_level += 1
            for stmt in then_block["Block"]:
                self.visit(stmt, in_main)
            self.indent_level -= 1
            self.append_code("}\n", in_main)

            if else_block is not None:
                self.append_code("else {\n", in_main)
                self.indent_level += 1
                for stmt in else_block["Block"]:
                    self.visit(stmt, in_main)
                self.indent_level -= 1
                self.append_code("}\n", in_main)

    def visit_Loop(self, node, in_main):
        condition = node["Condition"]
        block = node["Block"]
        cond_code, _ = self.generate_expression(condition)
        line = f"while ({cond_code}) {{\n"
        self.append_code(line, in_main)
        self.indent_level += 1
        for stmt in block["Block"]:
            self.visit(stmt, in_main)
        self.indent_level -= 1
        self.append_code("}\n", in_main)

    def visit_FunctionDef(self, node, in_main):
        func_name = node["Name"]
        parameters = node["Parameters"]
        body = node["Body"]

        old_main_code = self.main_code
        old_indent = self.indent_level
        old_variables = self.variables.copy()
        old_in_function = self.in_function_definition
        old_return_type = self.current_function_return_type

        self.main_code = ""
        self.indent_level = 1
        self.variables = {}
        self.in_function_definition = True
        self.current_function_return_type = None
        params_code = ", ".join([f"int {p}" for p in parameters])

        for stmt in body["Block"]:
            self.visit(stmt, in_main=False)

        if self.current_function_return_type is None:
            self.current_function_return_type = "int"
            if "return" not in self.main_code:
                self.main_code += f"{self.indent()}return 0;\n"

        if "[]" in self.current_function_return_type:
            raise Exception(f"Error: Function '{func_name}' returns an array, which is not allowed.")

        c_return_type = self.map_type(self.current_function_return_type)
        func_code = f"{c_return_type} {func_name}({params_code}) {{\n"
        func_code += self.main_code
        func_code += "}\n\n"

        self.function_return_type[func_name] = self.current_function_return_type

        self.main_code = old_main_code
        self.indent_level = old_indent
        self.variables = old_variables
        self.in_function_definition = old_in_function
        self.current_function_return_type = old_return_type

        self.functions_code += func_code

    def visit_EmptyStatement(self, node, in_main):
        self.append_code(";\n", in_main)

    def visit_Block(self, node, in_main):
        for stmt in node["Block"]:
            self.visit(stmt, in_main)

    def generate_expression(self, expr):
        node_type = list(expr.keys())[0]
        node_value = expr[node_type]

        if node_type == "IntegerLiteral":
            return (str(node_value), "int")
        elif node_type == "FloatLiteral":
            return (str(node_value), "float")
        elif node_type == "StringLiteral":
            string_val = node_value
            if string_val.startswith('"') and string_val.endswith('"'):
                string_val = string_val[1:-1]
            return (f"\"{string_val}\"", "string")
        elif node_type == "Identifier":
            # Variable -> can't be determined at compile time for sure
            var_name = node_value
            var_type = self.variables.get(var_name, "int")
            return (var_name, self.reverse_map_type(var_type))
        elif node_type == "IndexedIdentifier":
            # Indexed access -> can't be determined at compile time for sure
            ident = node_value["Identifier"]
            index_expr = node_value["Index"]
            index_code, _ = self.generate_expression(index_expr)
            return (f"{ident}[{index_code}]", "int")
        elif node_type == "FunctionCall":
            # Function calls -> cannot determine at compile time
            func_name = node_value["Name"]
            args = node_value["Arguments"]
            args_code = []
            for arg in args:
                arg_code, _ = self.generate_expression(arg)
                args_code.append(arg_code)
            ret_type = self.function_return_type.get(func_name, "int")
            return (f"{func_name}({', '.join(args_code)})", ret_type)
        elif node_type == "Term":
            left_node = node_value["Left"]
            op = node_value["Operator"]
            right_node = node_value["Right"]
            left_code, left_type = self.generate_expression(left_node)
            right_code, right_type = self.generate_expression(right_node)
            result_type = self.pick_numeric_type(left_type, right_type)
            return self.constant_fold(left_code, right_code, op, result_type)
        elif node_type == "ArithmeticExpression":
            left_node = node_value["Left"]
            op = node_value["Operator"]
            right_node = node_value["Right"]
            left_code, left_type = self.generate_expression(left_node)
            right_code, right_type = self.generate_expression(right_node)
            result_type = self.pick_numeric_type(left_type, right_type)
            return self.constant_fold(left_code, right_code, op, result_type)
        elif node_type == "RelationalExpression":
            left_node = node_value["Left"]
            op = node_value["Operator"]
            right_node = node_value["Right"]
            left_code, left_type = self.generate_expression(left_node)
            right_code, right_type = self.generate_expression(right_node)
            # Just return code, can't fold relational here easily
            return (f"({left_code} {op} {right_code})", "int")
        elif node_type == "UnaryExpression":
            op = node_value["Operator"]
            operand = node_value["Operand"]
            operand_code, operand_type = self.generate_expression(operand)
            if op == '-' and self.is_numeric_literal(operand_code):
                if '.' in operand_code:
                    val = float(operand_code)
                    return (str(-val), operand_type)
                else:
                    val = int(operand_code)
                    return (str(-val), operand_type)
            return (f"({op}{operand_code})", operand_type)
        elif node_type == "ListExpression":
            element_type = node_value["Type"]
            elements = node_value["Elements"]
            c_elements = []
            for elem in elements:
                elem_code, elem_type = self.generate_expression(elem)
                c_elements.append(elem_code)
            c_type = self.map_type(element_type)
            return (c_elements, c_type + "[]")
        else:
            raise Exception(f"Unknown expression node type: {node_type}")

    def evaluate_condition_if_purely_numeric(self, condition_expr):
        """
        Attempt to evaluate the if condition at compile time if it's purely numeric.
        If we can determine it's always True or always False, return True or False.
        If we cannot determine, return None.
        """
        # We can try a simplified approach:
        # - If the condition is a relational expression of only numeric literals,
        #   we evaluate it now.
        # Otherwise, return None.

        # Extract expression
        node_type = list(condition_expr.keys())[0]
        if node_type == "RelationalExpression":
            node_value = condition_expr[node_type]
            left = node_value["Left"]
            op = node_value["Operator"]
            right = node_value["Right"]

            left_code, left_type = self.generate_expression(left)
            right_code, right_type = self.generate_expression(right)

            # If both sides are numeric literals, we can compare
            if self.is_numeric_literal(left_code) and self.is_numeric_literal(right_code):
                left_val = float(left_code) if '.' in left_code else int(left_code)
                right_val = float(right_code) if '.' in right_code else int(right_code)
                if op == "<":
                    return left_val < right_val
                elif op == ">":
                    return left_val > right_val
                elif op == "<=":
                    return left_val <= right_val
                elif op == ">=":
                    return left_val >= right_val
                elif op == "==":
                    return left_val == right_val
                elif op == "!=":
                    return left_val != right_val

        # If not handled, return None indicating we can't determine at compile time
        return None

    def map_type(self, expr_type):
        if expr_type == "int":
            return "int"
        elif expr_type == "float":
            return "double"
        elif expr_type == "string":
            return "char*"
        else:
            return "int"

    def reverse_map_type(self, c_type):
        if c_type == "int":
            return "int"
        elif c_type == "double":
            return "float"
        elif c_type == "char*":
            return "string"
        return "int"

    def pick_numeric_type(self, left_type, right_type):
        if left_type == "float" or right_type == "float":
            return "float"
        return "int"

    def append_code(self, line, in_main=False):
        if self.in_function_definition:
            self.main_code += self.indent() + line
        else:
            self.main_code += self.indent() + line

    def constant_fold(self, left_code, right_code, op, result_type):
        if self.is_numeric_literal(left_code) and self.is_numeric_literal(right_code):
            left_val = float(left_code) if '.' in left_code else int(left_code)
            right_val = float(right_code) if '.' in right_code else int(right_code)

            if op == '+':
                val = left_val + right_val
            elif op == '-':
                val = left_val - right_val
            elif op == '*':
                val = left_val * right_val
            elif op == '/':
                if right_val == 0:
                    # Can't fold division by zero
                    return (f"({left_code} {op} {right_code})", result_type)
                val = left_val / right_val if result_type == "float" else left_val // right_val
            else:
                return (f"({left_code} {op} {right_code})", result_type)

            if result_type == "int":
                val = int(val)
            return (str(val), result_type)
        else:
            return (f"({left_code} {op} {right_code})", result_type)

    def is_numeric_literal(self, code_str):
        clean = code_str.strip("()")
        if clean.startswith('-'):
            clean = clean[1:]
        return clean.replace('.', '', 1).isdigit()

if __name__ == "__main__":
    ast = json.load(sys.stdin)
    generator = CodeGenerator(ast)
    c_code = generator.generate_code()
    print(c_code)
