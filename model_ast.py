from dataclasses import dataclass
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
class Program(Stmt):
  functions : List[Stmt]

@dataclass
class Function(Stmt):
  id         : str
  arguments  : List[Expr]
  variables  : List[Expr]
  statements : List[Stmt]

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
  left  : Expr
  right : Expr

@dataclass
class Not(Expr):
  key   : str
  rel   : Expr

@dataclass
class Binary(Expr):
  op    : str
  left  : Expr
  right : Expr

@dataclass
class Unary(Expr):
  op    : str
  expr  : Expr

@dataclass
class Call(Expr):
  id   : str
  expr : List[Expr]

@dataclass
class Assign(Stmt):
  loct : str
  expr : Expr

@dataclass
class Var(Expr):
  id   : str
  type : str

@dataclass
class VectorVar(Expr):
  id   : str
  type : str
  size : int

@dataclass
class Integer(Expr):
  value : int

@dataclass
class Float(Expr):
  value : float

@dataclass
class Vector(Expr):
  id   : str
  index : int

@dataclass
class Ident(Expr):
  id : str

@dataclass
class String(Expr):
  value : str

@dataclass
class DataType(Type):
  type : str