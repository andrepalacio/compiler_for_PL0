from model_ast import *


class IntermediateCodeGenerator:
    def __init__(self):
        self.target = 1
        self.code = []
        self.stack = []

    def visit(self, node: Literal):
        value, target = node.value, self.target
        if node.type == 'int':
          self.code.append(f"MOVI {value }, {target}")
        elif node.type == 'float':
          self.code.append(f"MOVF {value}, {target}")
        self.target += 1

    def visit(self, node: Var):
        name = node.id
        if node.type == 'int':
          self.code.append(f"VARI {name}")
        elif node.type == 'float':
          self.code.append(f"VARF {name}")
        self.stack.append(node)

    def visit(self, node: Ident):
        name = node.name
        self.code.append(f"ALLOCI {name}")

    def visit_LOADI(self, node):
        name, target = node.name, node.target
        self.code.append(f"LOADI {name}, {target}")

    def visit_STOREI(self, node):
        target, name = node.target, node.name
        self.code.append(f"STOREI {target}, {name}")

    # Implement the remaining visit methods for other instructions...

    def generate_code(self, ast):
        for node in ast:
            self.visit(node)

        return self.code
