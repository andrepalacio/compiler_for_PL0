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
from model import *

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

@dataclass
class Literal(Expression):
	...

@dataclass
class Integer(Literal):
	value : int
	dtype : DataType = SimpleType('int')

@dataclass
class Float(Literal):
	value : float
	dtype : DataType = SimpleType('float')



class Checker(Visitor):

	def visit(self, n: Literal, env: Symtab):
		# Devolver datatype

	def visit(self, n: Location, env: Symtab):
		# Buscar en Symtab y extraer datatype (No se encuentra?)
		# Devuelvo el datatype

	def visit(self, n: TypeCast, env: Symtab):
		# Visitar la expresion asociada
		# Devolver datatype asociado al nodo

	def visit(self, n: Assign, env: Symtab):
		# Visitar el hijo izquierdo (devuelve datatype)
		# Visitar el hijo derecho (devuelve datatype)
		# Comparar ambos tipo de datatype

	def visit(self, n: FuncCall, env: Symtab):
		# Buscar la funcion en Symtab (extraer: Tipo de retorno, el # de parametros)
		# Visitar la lista de Argumentos
		# Comparar el numero de argumentos con parametros
		# Comparar cada uno de los tipos de los argumentos con los parametros
		# Retornar el datatype de la funcion

	def visit(self, n: Binary, env: Symtab):
		# Visitar el hijo izquierdo (devuelve datatype)
		# Visitar el hijo derecho (devuelve datatype)
		# Comparar ambos tipo de datatype

	def visit(self, n: Logical, env: Symtab):
		# Visitar el hijo izquierdo (devuelve datatype)
		# Visitar el hijo derecho (devuelve datatype)
		# Comparar ambos tipo de datatype

	def visit(self, n: Unary, env: Symtab):
		# Visitar la expression asociada (devuelve datatype)
		# Comparar datatype

	def visit(self, n: FuncDefinition, env: Symtab):
		# Agregar el nombre de la funcion a Symtab
		# Crear un nuevo contexto (Symtab)
		# Visitar ParamList, VarList, StmtList
		# Determinar el datatype de la funcion (revisando instrucciones return)

	def visit(self, n: VarDefinition, env: Symtab):
		# Agregar el nombre de la variable a Symtab

	def visit(self, n: Parameter, env: Symtab):
		# Agregar el nombre del parametro a Symtab

	def visit(self, n: Print, env: Symtab):
		...		

	def visit(self, n: Write, env: Symtab):
		# Buscar la Variable en Symtab

	def visit(self, n: Read, env: Symtab):
		# Buscar la Variable en Symtab

	def visit(self, n: While, env: Symtab):
		# Visitar la condicion del While (Comprobar tipo bool)
		# Visitar las Stmts

	def visit(self, n: Break, env: Symtab):
		# Esta dentro de un While?

	def visit(self, n: IfStmt, env: Symtab):
		# Visitar la condicion del IfStmt (Comprobar tipo bool)
		# Visitar las Stmts del then y else

	def visit(self, n: Return, env: Symtab):
		# Visitar la expresion asociada
		# Actualizar el datatype de la funcion

	def visit(self, n: Skip, env: Symtab):
		...

	def visit(self, n: Program, env: Symtab):
		# Crear un nuevo contexto (Symtab global)
		# Visitar cada una de las declaraciones asociadas

	def visit(self, n: StmtList, env: Symtab):
		# Visitar cada una de las instruciones asociadas

	def visit(self, n: VarList, env: Symtab):
		# Visitar cada una de las variables asociadas

	def visit(self, n: ParmList, env: Symtab):
		# Visitar cada una de los parametros asociados

	def visit(self, n: ArgList, env: Symtab):
		# Visitar cada una de los argumentos asociados
