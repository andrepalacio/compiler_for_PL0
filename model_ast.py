from dataclasses import dataclass
from typing import List


# Clases Abstractas

@dataclass
class Node:
  ...

@dataclass
class Function(Node):
  ...

@dataclass
class Statement(Node):
  ...

@dataclass
class Expr(Node):
  ...

# Clases concretas
@dataclass
class Program(Function):
  functions : List[Function]

@dataclass
class Function(Function):
  id         : str
  args       : List[Expr]
  variables  : List[Expr]
  statements : List[Statement]

@dataclass
class OneStatement(Statement):
  key   : str
  left  : Statement

@dataclass
class DualStatement(Statement):
  keyLeft   : str
  left      : Statement
  keyRight  : str
  right     : Statement

@dataclass
class TripleStatement(Statement):
  keyLeft   : str
  left      : Statement
  keyMiddle : str
  middle    : Statement
  keyRight  : str
  right     : Statement

@dataclass
class Join(Statement):
  keyLeft     : Statement
  statements  : List[Statement]
  keyRight    : Statement

@dataclass
class Single(Statement):
  key   : str

@dataclass
class StatementList(Statement):
  statements : List[Statement]

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
class ExprList(Expr):
  expr : List[Expr]

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
class Call(Statement):
  id   : str
  expr : List[Expr]

@dataclass
class Assign(Statement):
  id   : str
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