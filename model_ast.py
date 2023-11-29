from dataclasses import dataclass, field
from multimethod import multimeta
from typing import List


# Clase Visitor
class Visitor(metaclass=multimeta):
  ...


# Clases Abstractas
@dataclass
class Node:
  def accept(self, v:Visitor, *args, **kwargs):
    return v.visit(self, *args, **kwargs)

@dataclass
class Stmt(Node):
  ...

@dataclass
class Expr(Node):
  ...

@dataclass
class Type(Node):
  ...

# Clases concretas
@dataclass
class DataType(Type):
  type : str

@dataclass
class Program(Stmt):
  functions : List[Stmt]

@dataclass
class Function(Stmt):
  id          : str
  parameters  : List[Expr]
  variables   : List[Expr]
  statements  : List[Stmt]
  dtype       : DataType = field(default_factory=lambda: DataType(None))

@dataclass
class OneStmt(Stmt):
  key   : str
  value  : Stmt

@dataclass
class DualStmt(Stmt):
  keyLeft   : str
  left      : Stmt
  keyRight  : str
  right     : Stmt

@dataclass
class TripleStmt(Stmt):
  keyLeft   : str
  left      : Stmt
  keyMiddle : str
  middle    : Stmt
  keyRight  : str
  right     : Stmt

@dataclass
class Grouping(Expr):
  begin : str
  expr  : Expr
  end   : str

@dataclass
class Single(Stmt):
  key   : str

@dataclass
class Relation(Expr):
  rel    : str
  left   : Expr
  right  : Expr
  dtype  : DataType = field(default_factory=lambda: DataType(None))

@dataclass
class Not(Expr):
  key   : str
  rel   : Expr

@dataclass
class Binary(Expr):
  op    : str
  left  : Expr
  right : Expr
  dtype : DataType = field(default_factory=lambda: DataType(None))

@dataclass
class Unary(Expr):
  op    : str
  expr  : Expr
  dtype : DataType = field(default_factory=lambda: DataType(None))

@dataclass
class TypeCast(Unary):
  ...

@dataclass
class Call(Expr):
  id   : str
  expr : List[Expr]


@dataclass
class Var(Expr):
  id   : str
  type : DataType

@dataclass
class VectorVar(Var):
  id   : str
  type : DataType
  size : Expr

@dataclass 
class Ident(Expr):
  id   : str

@dataclass
class Vector(Ident):
  id   : str
  index : Expr

@dataclass
class Assign(Stmt):
  loct : Ident
  expr : Expr

@dataclass
class Literal(Expr):
	...

@dataclass
class Integer(Literal):
	value : int
	dtype : DataType('int')

@dataclass
class Float(Literal):
	value : float
	dtype : DataType('float')

# Clase Tree

""" class Tree(Visitor):
  def __init__(self, ast):
    self.ast = ast

  def visit(self, n:Program):
    print("Program", type(n))
    print(" +-- funclist")
    for stmt in n.functions:
      stmt.accept(self)

  def visit(self, n:Function):
    print(f"     +-- function ({n.id})")
    print(f"         | -- parmlist")
    for arg in n.arguments:
      arg.accept(self)
    print(f"         | -- varlist")
    for var in n.variables:
      var.accept(self)
    print(f"         | -- statements")
    for stmt in n.statements:
      stmt.accept(self)

  def visit(self, n:OneStmt):
    print(f"             +-- {n.key}")
    n.value.accept(self)

  def visit(self, n:DualStmt):
    print(f"             +-- {n.keyLeft}")
    n.left.accept(self)
    print(f"             +-- {n.keyRight}")
    n.right.accept(self)

  def visit(self, n:TripleStmt):
    print(f"             +-- {n.keyLeft}")
    n.left.accept(self)
    print(f"             +-- {n.keyMiddle}")
    n.middle.accept(self)
    print(f"             +-- {n.keyRight}")
    n.right.accept(self)

  def visit(self, n:Grouping):
    print(f"                 +-- {n.begin}")
    for expr in n.expr:
      expr.accept(self)
    print(f"                 +-- {n.end}")

  def visit(self, n:Single):
    print(f"                 +-- {n.key}")

  def visit(self, n:Relation):
    print("                 +-- Relation")
    n.left.accept(self)
    print(f"                      +-- {n.rel}")
    n.right.accept(self)

  def visit(self, n:Not):
    print(f"                 +-- {n.key}")
    n.rel.accept(self)

  def visit(self, n:Binary):
    print("                 +-- Binary")
    n.left.accept(self)
    print(f"                      +-- {n.op}")
    n.right.accept(self)

  def visit(self, n:Unary):
    print("                 +-- Binary")
    print(f"                 +-- {n.op}")
    n.expr.accept(self)

  def visit(self, n:Call):
    print("                 +-- Call")
    print(f"                 +-- {n.id}")
    for expr in n.expr:
      expr.accept(self)

  def visit(self, n:Assign):
    print("                 +-- Assign")
    n.loct.accept(self)
    n.expr.accept(self)

  def visit(self, n:Var):
    print(f"                 +-- id({n.id})")
    n.type.accept(self)

  def visit(self, n:VectorVar):
    print(f"                 +-- id({n.id})")
    n.type.accept(self)
    print(f"                 +-- id({n.size})")

  def visit(self, n:Vector):
    print(f"                 +-- id ({n.id})")
    print(f"                 +-- size")
    n.index.accept(self)

  def visit(self, n:String):
    print(f"                 +-- {n.value}")

  def visit(self, n:DataType):
    print(f"                      +-- {n.type}")
  
  @classmethod
  def print(cls, ast):
    vis = cls(ast)
    return ast.accept(vis) """