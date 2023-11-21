# checker.py
'''
Revision de Variables

Recorre el AST para determinar el alcance adecuado para cada simbol.

TODO: Podría agregar más manejo de errores.  Mejor manejo de mensajes de error.

En este proyecto necesita realizar comprobaciones semánticas en su programa.
Este problema es multifacético y complicado. Para que el cerebro no explote un poco menos, debes tomarlo con calma y en porciones pequeñas.
La esencia básica de lo que debe hacer es la siguiente:

1. Nombres y Simbolos:

	Todos los identificadores deben ser definidos antes de que ellos sean usados. Esto incluye variables, constantes y nombres de tipo. Pro ejemplo, esta clase de codigo genera un error:

		fun main()
		begin
			a := 3    /* Error. 'a' no definida.
		end

2. Tipos de literales y constantes

	Todos los símbolos literales se escriben implícitamente y se les debe asignar un tipo de "int" o "float". Este tipo se utiliza para establecer el tipo de constantes. Por ejemplo:

		fun main()
			const a = 42;         // Tipo "int"
			const b = 4.2;        // Tipo "float"
		begin
			skip
		end

3. Comprobar el tipo del operador

	Los operadores binarios sólo operan con operandos de un tipo compatible.
	De lo contrario, obtendrá un error de tipo. Por ejemplo:

		fun main()
			a : int;
			b : float;
			c : int;
			d : int;
			e : int;
		begin
			a := 2;
			b := 3.14;
			c := a + 3;    // OK
			d := a + b;    // Error.  int + float
			e := b + 4.5;  // Error.  int = float
		end

	Además, debe asegurarse de que solo se permitan operadores compatibles.

4.  Asignacion.

	Los lados izquierdo y derecho de una operación de asignación deben declararse como del mismo tipo.

		fun main()
			a : int;
		begin
			a = 4 + 5;     // OK
			a = 4.5;       // Error. int = float
		end

	Los valores sólo se pueden asignar a declaraciones de variables, no a constantes.

		fun main()
			a : int;
			const b = 42;
		begin
			a := 37;        // OK
			b := 37;        // Error. b is const
		end

Estrategia de implementacion:
------------------------
Utilizará la clase `Visitor` definida en pl0/model.py para recorrer el árbol de análisis. Definirá varios métodos para diferentes tipos de nodos AST. Por ejemplo, si tienes un nodo Binary, escribirás un método como este:

	def visit(self, n:Binary):
		...

Para comenzar, haga que cada método simplemente imprima un mensaje:

	def visit(self, n:Binary):
		print('visit:', n)
		n.left.accept(self)
		n.right.accept(self)

Esto al menos le indicará que el método se está activando. Pruebe algunos ejemplos de código simples y asegúrese de que todos sus métodos se estén ejecutando realmente cuando recorra el árbol de análisis.

Pruebas
-------
Los archivos test3/*.pl0 contienen diferentes cosas que debes verificar. Se dan instrucciones específicas en cada archivo de prueba.

Consejos generales
------------------
Lo principal en lo que debe pensar al verificar es en la corrección del programa. ¿Tiene sentido esta declaración u operación que está viendo en el árbol de análisis? De lo contrario, es necesario generar algún tipo de error. Utilice sus propias experiencias como programador como guía (piense en lo que causaría un error en su lenguaje de programación favorito).

Un desafío será la gestión de muchos detalles complicados.
Tienes que realizar un seguimiento de símbolos, tipos y diferentes tipos de capacidades.
No siempre está claro cómo organizar mejor todo eso. Por lo tanto, espere andar un poco a tientas al principio.


::: AST :::
	|
	+-- Node
			|
			+-- DataType
			|   |
			|   +-- SimpleType : 'int', 'float'
			|   |
			|   +-- ArrayType : 'int[]', 'float[]'
			|
			+-- Expression
			|   |
			|   +-- Literal
			|   |   |
			|   |   +-- Integer : 12, 34, 23
			|   |   |
			|   |   +-- Float : 3.14, 1.618
			|   |
			|   +-- Location
			|   |   |
			|   |   +-- SimpleLocation : 'a', 'b', 'casa',
			|   |   |
			|   |   +-- ArrayLocation
			|   |
			|   +-- TypeCast
			|   |
			|   +-- Assign
			|   |
			|   +-- FuncCall
			|   |
			|   +-- Binary
			|   |
			|   +-- Logical
			|   |
			|   +-- Unary
			|
			+-- Statement
					|
					+-- Declaration
					|   |
					|   +-- FuncDefinition
					|   |
					|   +-- VarDefinition
					|   |
					|   +-- Parameter
					|
					+-- Print
					|
					+-- Write
					|
					+-- Read
					|
					+-- While
					|
					+-- Break
					|
					+-- IfStmt
					|
					+-- Return
					|
					+-- Skip
					|
					+-- Program
					|
					+-- StmtList
					|
					+-- VarList
					|
					+-- ParmList
					|
					+-- ArgList

'''
#checker.py
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

	def __init__(self, parent=None):
		'''
		Crea una tabla de símbolos vacia con la tabla de
		simbolos padre dada.
		'''
		self.entries = {}
		self.parent = parent
		self.dtype = None
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
		self.dtype = type

	def add_child(self, child):
		'''
		Agrega una tabla de simbolos secundaria a esta tabla de
		simbolos.
		'''
		self.children.append(child)


class Checker(Visitor):

	def visit(self, n: Literal, env: Symtab):
		return n.dtype

	def visit(self, n: Ident, env: Symtab):
		node = env.get(n.id)
		if node != None:
			return node.type.type
		else:
			raise NameError("ID not found")

	def visit(self, n: TypeCast, env: Symtab):
		# Visitar la expresion asociada
		# Devolver datatype asociado al nodo
		expr_data = n.expr.accept()
		if expr_data != None:
			n.dtype = DataType(n.op)
			return n.op
		raise Exception("Expression can not be processed")


	def visit(self, n: Assign, env: Symtab):
		# Visitar el hijo izquierdo (devuelve datatype)
		# Visitar el hijo derecho (devuelve datatype)
		# Comparar ambos tipo de datatype
		ident = n.loct.accept()
		expr = n.expr.accept()
		if ident != expr:
			raise Exception("Invalid Datatypes")
		return ident

	def visit(self, n: Call, env: Symtab):
		# Buscar la funcion en Symtab (extraer: Tipo de retorno, el # de parametros)
		# Visitar la lista de Argumentos
		# Comparar el numero de argumentos con parametros
		# Comparar cada uno de los tipos de los argumentos con los parametros
		# Retornar el datatype de la funcion
		pass

	def visit(self, n: Relation, env: Symtab):
		# Visitar el hijo izquierdo (devuelve datatype)
		# Visitar el hijo derecho (devuelve datatype)
		# Comparar ambos tipo de datatype
		ident = n.loct.accept()
		expr = n.expr.accept()
		if expr != None and ident != None:
			if ident == expr:
				n.dtype = DataType('bool')
				return n.dtype
		raise Exception("Invalid Datatypes")
	
	def visit(self, n: Binary, env: Symtab):
		# Visitar el hijo izquierdo (devuelve datatype)
		# Visitar el hijo derecho (devuelve datatype)
		# Comparar ambos tipo de datatype
		ident = n.loct.accept()
		expr = n.expr.accept()
		if ident != expr or ident == None or expr == None:
			raise Exception("Invalid Datatypes in Binary")
		n.dtype = DataType(ident)
		return n.dtype

	def visit(self, n: Unary, env: Symtab):
		# Visitar la expression asociada (devuelve datatype)
		# Comparar datatype
		expr_type = n.expr.accept()
		if expr_type == None:
			raise Exception("Error in type")
		n.dtype = DataType(expr_type)
		return n.dtype

	def visit(self, n: Function, env: Symtab):
		# Agregar el nombre de la funcion a Symtab
		# Crear un nuevo contexto (Symtab)
		# Visitar ParamList, VarList, StmtList
		# Determinar el datatype de la funcion (revisando instrucciones return)
		env.add(n.id, n)
		new_env = Symtab(env)
		env.add_child(new_env)
		for param in n.params:
			param.accept(new_env)
		for var in n.vars:
			var.accept(new_env)
		for stmt in n.stmts:
			stmt.accept(new_env)
		return new_env.dtype

	def visit(self, n: Var, env: Symtab):
		# Agregar el nombre de la variable a Symtab
		env.add(n.id, n)

	# def visit(self, n: Parameter, env: Symtab):
		# Agregar el nombre del parametro a Symtab

	def visit(self, n: OneStmt, env: Symtab):
		info_type = n.value.accept()
		if info_type == None:
			raise NameError("Variable not found")
		if n.key == 'return':
			# Actualizar el datatype de la funcion
			env.return_type(info_type)
		return info_type
		

	def visit(self, n: DualStmt, env: Symtab):
		# Visitar la condicion del While (Comprobar tipo bool)
		# Visitar las Stmts
		bool_type = n.left.accept()
		if bool_type == None:
			raise Exception("Invalid Datatype in condition")
		expr_type = n.right.accept()
		if expr_type == 'break' or expr_type == 'skip' :
				if n.key != 'while':
					raise Exception("Invalid Break or Skip")
		if expr_type == None:
			raise Exception("Invalid Datatype in statements")
		return bool_type

	def visit(self, n: TripleStmt, env: Symtab):
		# Visitar la condicion del IfStmt (Comprobar tipo bool)
		# Visitar las Stmts del then y else
		bool_type = n.left.accept()
		if bool_type == None:
			raise Exception("Invalid Datatype in condition")
		expr1_type = n.middle.accept()
		expr2_type = n.right.accept()
		if expr1_type == None or expr2_type == None:
			raise Exception("Invalid Datatype in statements")
		return bool_type

	def visit(self, n: Single, env: Symtab):
		return n.key
	
	def visit(self, n: Grouping, env: Symtab):
		# Visitar las Stmts
		returning = None
		for stmt in n.expr:
			info = stmt.accept()
			if info == 'skip' or info == 'break':
				returning = info
			elif info != None and returning == None:
				returning = info
		return returning

	def visit(self, n: Program, env: Symtab):
		# Crear un nuevo contexto (Symtab global)
		# Visitar cada una de las declaraciones asociadas
		# Verificar si existe la funcion main
		new_env = Symtab(env)
		for func in n.functions:
			func.accept(new_env)
		if new_env.get('main') == None:
			raise Exception("Main function not found")
