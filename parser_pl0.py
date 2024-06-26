from sly import Parser
from sys import argv
from rich import print as rprint
from lexer_pl0 import LexerForPL0, print_lexer
from model_ast import *

class ParserForPL0(Parser):
  #expected_shift_reduce = 1
  debugfile = 'parserPL0.txt'

  precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'GT', 'GTE', 'LT', 'LTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'NOT', 'UNARY')
  )

  tokens = LexerForPL0.tokens

  # grammar rules implementation

  @_('funcList')
  def program(self, p):
    return Program(p.funcList)
  
  @_('func funcList')
  def funcList(self, p):
    return [p.func] + p.funcList
  
  @_('func')
  def funcList(self, p):
    return [p.func]
  
  @_('FUN ID LPAREN paramList RPAREN varList BEGIN statementList END')
  def func(self, p):
    return Function(p.ID, p.paramList, p.varList, p.statementList)
  
  @_('FUN ID LPAREN RPAREN varList BEGIN statementList END')
  def func(self, p):
    return Function(p.ID, [], p.varList, p.statementList)
  
  @_('FUN ID LPAREN paramList RPAREN BEGIN statementList END')
  def func(self, p):
    return Function(p.ID, p.paramList, [], p.statementList)
  
  @_('FUN ID LPAREN RPAREN BEGIN statementList END')
  def func(self, p):
    return Function(p.ID, [], [], p.statementList)
  
  @_('statements SEMICOLON statementList')
  def statementList(self, p):
    return p.statements + p.statementList
  
  @_('statements')
  def statementList(self, p):
    return p.statements
  
  @_('statement', 'noStatement')
  def statements(self, p):
    return [p[0]]

  @_('WHILE relation DO statement')
  def statement(self, p):
    return DualStmt(p.WHILE, p.relation, p.DO, p.statement)

  @_('IF relation THEN statement ELSE statement')
  def statement(self, p):
    return TripleStmt(p.IF, p.relation, p.THEN, p[3], p.ELSE, p[5])

  @_('location ASSIGN expr')
  def statement(self, p):
    return Assign(p.location, p.expr)

  @_('PRINT LPAREN STRING RPAREN')
  def statement(self, p):
    return OneStmt(p.PRINT, p.STRING)

  @_('WRITE LPAREN expr RPAREN')
  def statement(self, p):
    return OneStmt(p.WRITE, p.expr)

  @_('READ LPAREN location RPAREN')
  def statement(self, p):
    return OneStmt(p.READ, p.location)

  @_('RETURN expr')
  def statement(self, p):
    return OneStmt(p.RETURN, p.expr)

  @_('ID LPAREN exprList RPAREN')
  def statement(self, p):
    return Call(p.ID, p.exprList)
  
  @_('ID LPAREN RPAREN')
  def statement(self, p):
    return Call(p.ID, [])

  @_('SKIP')
  def statement(self, p):
    return Single(p.SKIP)

  @_('BREAK')
  def statement(self, p):
    return Single(p.BREAK)

  @_('BEGIN statementList END')
  def statement(self, p):
    return Grouping(p.BEGIN, p.statementList, p.END)
  
  @_('IF relation THEN statement')
  def noStatement(self, p):
    return DualStmt(p.IF, p.relation, p.THEN, p.statement)

  @_('relExpr AND relation', 'relExpr OR relation')
  def relation(self, p):
    return Relation(p[1], p[0], p[2])
  
  @_('relExpr')
  def relation(self, p):
    return p.relExpr
  
  @_('expr relCon expr')
  def relExpr(self, p):
    return Relation(p[1], p[0], p[2])
  
  @_('LTE', 'LT', 'GTE', 'GT', 'EQ', 'NEQ')
  def relCon(self, p):
    return p[0]
  
  @_('NOT relation')
  def relation(self, p):
    return Not(p.NOT, p.relation)
  
  @_('LPAREN relation RPAREN')
  def relation(self, p):
    return p.relation

  @_('expr COMMA exprList')
  def exprList(self, p):
    return [p.expr] + p.exprList

  @_('expr')
  def exprList(self, p):
    return [p.expr]

  @_('expr PLUS expr', 'expr MINUS expr', 'expr TIMES expr', 'expr DIVIDE expr')
  def expr(self, p):
    return Binary(p[1], p[0], p[2])
  
  @_('MINUS expr %prec UNARY', 'PLUS expr %prec UNARY')
  def expr(self, p):
    return Unary(p[0], p.expr)
  
  @_('LPAREN expr RPAREN')
  def expr(self, p):
    return p.expr
  
  @_('ID LPAREN exprList RPAREN')
  def expr(self, p):
    return Call(p.ID, p.exprList)
  
  @_('ID LPAREN RPAREN')
  def expr(self, p):
    return Call(p.ID, [])
  
  @_('ID')
  def expr(self, p):
    return Ident(p.ID)
  
  @_('ID LBRACKET expr RBRACKET')
  def expr(self, p):
    return Vector(p.ID, p.expr)
  
  @_('number')
  def expr(self, p):
    return p.number
  
  @_('TINT LPAREN expr RPAREN')
  def expr(self, p):
    return TypeCast(p.TINT, p.expr)
  
  @_('TFLOAT LPAREN expr RPAREN')
  def expr(self, p):
    return TypeCast(p.TFLOAT, p.expr)
  
  @_('varDecl COMMA paramList')
  def paramList(self, p):
    return [p.varDecl] + p.paramList

  @_('varDecl')
  def paramList(self, p):
    return [p.varDecl]
  
  @_('varDecl SEMICOLON varList', 'func SEMICOLON varList')
  def varList(self, p):
    return [p[0]] + p.varList
  
  @_('varDecl SEMICOLON', 'func SEMICOLON')
  def varList(self, p):
    return [p[0]]

  @_('ID COLON varType')
  def varDecl(self, p):
    return Var(p.ID, p.varType)
  
  @_('ID COLON vectorType')
  def varDecl(self, p):
    return VectorVar(p.ID, p.vectorType[0], p.vectorType[1])
  
  @_('TINT', 'TFLOAT')
  def varType(self, p):
    return DataType(p[0])
  
  @_('TINT LBRACKET expr RBRACKET', 'TFLOAT LBRACKET expr RBRACKET')
  def vectorType(self, p):
    return DataType(p[0]), p[2]

  @_('INT')
  def number(self, p):
    return Integer(p.INT, DataType('int'))
  
  @_('FLOAT')
  def number(self, p):
    return Float(p.FLOAT, DataType('float'))
  
  @_('ID')
  def location(self, p):
    return Ident(p.ID)
  
  @_('ID LBRACKET expr RBRACKET')
  def location(self, p):
    return Vector(p.ID, p.expr)
  

def gen_ast(text_input):
  lexer = LexerForPL0()
  parser = ParserForPL0()
  return parser.parse(lexer.tokenize(text_input))


if __name__ == '__main__':
  # import sys
  # sys.setrecursionlimit(5000)
  lexer = LexerForPL0()
  parser = ParserForPL0()
  filename = argv[1]
  with open(filename, 'r') as f:
    text_input = f.read()
    # print(text_input)
    # print_lexer(text_input)
    ast = parser.parse(lexer.tokenize(text_input))
    rprint(ast)
    # Tree.print(ast)

