#checker.py
# from model_ast import 
from model_ast import *

# ---------------------------------------------------------------------
#  Tabla de Simbolos
# ---------------------------------------------------------------------

class Symtab:
	'''
	Una tabla de símbolos.  Este es un objeto simple que sólo
	mantiene una hashtable (dict) de nombres de simbolos y los
	nodos de declaracion o definición de funciones a los que se
	refieren.
	Hay una tabla de simbolos separada para cada elemento de
	código que tiene su propio contexto (por ejemplo cada función,
	clase, tendra su propia tabla de simbolos). Como resultado,
	las tablas de simbolos se pueden anidar si los elementos de
	código estan anidados y las búsquedas de las tablas de
	simbolos se repetirán hacia arriba a través de los padres
	para representar las reglas de alcance léxico.
	'''
	class SymbolDefinedError(Exception):
		'''
		Se genera una excepción cuando el código intenta agregar
		un simbol a una tabla donde el simbol ya se ha definido.
		Tenga en cuenta que 'definido' se usa aquí en el sentido
		del lenguaje C, es decir, 'se ha asignado espacio para el
		simbol', en lugar de una declaración.
		'''
		pass

	def __init__(self, name=None, parent=None):
		'''
		Crea una tabla de símbolos vacia con la tabla de
		simbolos padre dada.
		'''
		self.name = name
		self.entries = {}
		self.parent = parent
		if self.parent:
			self.parent.children.append(self)
		self.children = []

	def add(self, name, value):
		'''
		Agrega un simbol con el valor dado a la tabla de simbolos.
		El valor suele ser un nodo AST que representa la declaración
		o definición de una función, variable (por ejemplo, Declaración
		o FuncDeclaration)
		'''
		if name in self.entries:
			raise Symtab.SymbolDefinedError()
		self.entries[name] = value

	def get(self, name):
		'''
		Recupera el símbol con el nombre dado de la tabla de
		simbol, recorriendo hacia arriba a traves de las tablas
		de simbol principales si no se encuentra en la actual.
		'''
		if name in self.entries:
			return self.entries[name]
		elif self.parent:
			return self.parent.get(name)
		return None
	
	def return_type(self, type):
		if self.parent:
			node = self.parent.get(self.name)
			node.dtype = DataType(type)


class Checker(Visitor):

	def __init__(self, ast):
		self.ast = ast

	def visit(self, n: Literal, env: Symtab):
		return n.dtype.type

	def visit(self, n: Ident, env: Symtab):
		node = env.get(n.id)
		if node == None:
			raise NameError("ID not found")
		return node.type.type

	def visit(self, n: Vector, env: Symtab):
		node = env.get(n.id)
		if node == None:
			raise NameError("ID not found")
		index = n.index.accept(self, env)
		if index == 'int' and index >= 0 and index < node.size:
			return node.type.type
		else:
			raise Exception("Invalid index")

	def visit(self, n: TypeCast, env: Symtab):
		# Visitar la expresion asociada
		# Devolver datatype asociado al nodo
		expr_data = n.expr.accept(self, env)
		if expr_data != None:
			n.dtype = DataType(n.op)
			return n.op
		raise Exception("Expression can not be processed")

	def visit(self, n: Assign, env: Symtab):
		# Visitar el hijo izquierdo (devuelve datatype)
		# Visitar el hijo derecho (devuelve datatype)
		# Comparar ambos tipo de datatype
		ident = n.loct.accept(self, env)
		expr = n.expr.accept(self, env)
		if ident != expr:
			raise Exception("Invalid Datatypes")
		return ident

	def visit(self, n: Call, env: Symtab):
		# Buscar la funcion en Symtab (extraer: Tipo de retorno, el # de parametros)
		# Visitar la lista de Argumentos
		# Comparar el numero de argumentos con parametros
		# Comparar cada uno de los tipos de los argumentos con los parametros
		# Retornar el datatype de la funcion
		func = env.get(n.id)
		if func == None:
			raise Exception("Function not found")
		if len(func.parameters) != len(n.expr):
			raise Exception("Invalid number of arguments")
		for i in range(len(func.parameters)):
			func_param = func.parameters[i].type.type
			expr_param = n.expr[i].accept(self, env)
			if func_param != expr_param:
				raise Exception("Invalid Datatypes", func_param, expr_param)
		return func.dtype.type

	def visit(self, n: Relation, env: Symtab):
		# Visitar el hijo izquierdo (devuelve datatype)
		# Visitar el hijo derecho (devuelve datatype)
		# Comparar ambos tipo de datatype
		exprl = n.left.accept(self, env)
		exprr = n.right.accept(self, env)
		if exprl != None and exprr != None:
			if exprl == exprr:
				n.dtype = DataType(exprl)
				return n.dtype.type
		raise Exception("Invalid Datatypes")
	
	def visit(self, n: Not, env: Symtab):
		reld = n.rel.accept(self, env)
		if reld != None:
			raise NameError("ID not found")
		return reld.type
	
	def visit(self, n: Binary, env: Symtab):
		# Visitar el hijo izquierdo (devuelve datatype)
		# Visitar el hijo derecho (devuelve datatype)
		# Comparar ambos tipo de datatype
		left = n.left.accept(self, env)
		right = n.right.accept(self, env)
		if left != right or left == None or right == None:
			raise Exception("Invalid Datatypes in Binary")
		n.dtype = DataType(left)
		return n.dtype.type

	def visit(self, n: Unary, env: Symtab):
		# Visitar la expression asociada (devuelve datatype)
		# Comparar datatype
		expr_type = n.expr.accept(self, env)
		if expr_type == None:
			raise Exception("Error in type")
		n.dtype = DataType(expr_type)
		return n.dtype.type

	# def visit(self, n: Parameter, env: Symtab):
		# Agregar el nombre del parametro a Symtab

	def visit(self, n: OneStmt, env: Symtab):
		if n.key == 'print':
			if isinstance(n.value, str):
				return 'string'
		info_type = n.value.accept(self, env)
		if info_type == None:
			raise NameError("Variable not found")
		if n.key == 'return':
			# Actualizar el datatype de la funcion
			env.return_type(info_type)
		return info_type
		

	def visit(self, n: DualStmt, env: Symtab):
		# Visitar la condicion del While (Comprobar tipo bool)
		# Visitar las Stmts
		bool_type = n.left.accept(self, env)
		if bool_type == None:
			raise Exception("Invalid Datatype in condition")
		expr_type = n.right.accept(self, env)
		if expr_type == 'break' or expr_type == 'skip' :
				if n.key != 'while':
					raise Exception("Invalid Break or Skip")
		if expr_type == None:
			raise Exception("Invalid Datatype in statements")
		return bool_type

	def visit(self, n: TripleStmt, env: Symtab):
		# Visitar la condicion del IfStmt (Comprobar tipo bool)
		# Visitar las Stmts del then y else
		bool_type = n.left.accept(self, env)
		if bool_type == None:
			raise Exception("Invalid Datatype in condition")
		expr1_type = n.middle.accept(self, env)
		expr2_type = n.right.accept(self, env)
		if expr1_type == None or expr2_type == None:
			raise Exception("Invalid Datatype in statements")
		return bool_type

	def visit(self, n: Single, env: Symtab):
		return n.key
	
	def visit(self, n: Grouping, env: Symtab):
		# Visitar las Stmts
		returning = None
		for stmt in n.expr:
			info = stmt.accept(self, env)
			if info == 'skip' or info == 'break':
				returning = info
			elif info != None and returning == None:
				returning = info
		return returning

	def visit(self, n: Function, env: Symtab):
		# Agregar el nombre de la funcion a Symtab
		# Crear un nuevo contexto (Symtab)
		# Visitar ParamList, VarList, StmtList
		# Determinar el datatype de la funcion (revisando instrucciones return)
		env.add(n.id, n)
		new_env = Symtab(n.id, env)
		for param in n.parameters:
			param.accept(self, new_env)
		for var in n.variables:
			var.accept(self, new_env)
		for stmt in n.statements:
			stmt.accept(self, new_env)
		return n.dtype.type

	def visit(self, n: Var, env: Symtab):
		# Agregar el nombre de la variable a Symtab
		env.add(n.id, n)

	def visit(self, n: VectorVar, env: Symtab):
		# Agregar el nombre de la variable a Symtab
		env.add(n.id, n)

	def visit(self, n: Program, env: Symtab):
		for func in n.functions:
			func.accept(self, env)
		main = env.get('main')
		if main == None:
			raise Exception("Main function not found")
		return main.dtype.type

	@classmethod
	def check(cls, ast):
		vis = cls(ast)
		env = Symtab()
		return ast.accept(vis, env)
	
if __name__ == '__main__':
	import sys
	from lexer_pl0 import LexerForPL0
	from parser_pl0 import ParserForPL0
	from rich import print as rprint

	lexer = LexerForPL0()
	parser = ParserForPL0()

	with open(sys.argv[1]) as file:
	# with open('test3/fib.pl0') as file:
		source = file.read()
		ast = parser.parse(lexer.tokenize(source))

	#Tree.print(ast)
	# rprint(ast)
	Checker.check(ast)
	rprint(ast)
	#print(ast)
