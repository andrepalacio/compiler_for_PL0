import logging
from sly import Parser
from rich import print as rprint
from lexer_pl0 import LexerForPL0, print_lexer
from model_ast import *

class parserForPL0(Parser):
  #log = logging.getLogger()
  #log.setLevel(logging.ERROR)
  expected_shift_reduce = 1
  debugfile = 'parser.out'

  tokens = LexerForPL0.tokens

  # grammar rules implementation

  @_('funcList')
  def program(self, p):
    funcList = p.func.append(p.funcMain)
    return Program(funcList)
  
  @_('funcMain')
  def program(self, p):
    return Program(p.funcMain)
  
  @_('funcList func')
  def funcList(self, p):
    funcList = p.funcList.append(p.func)
    return funcList
  
  @_('func')
  def funcList(self, p):
    return p.func
  
  @_('FUN ID LPAREN argList RPAREN varList statementList')
  def func(self, p):
    return Function(p.ID, p.argList, p.varList, p.statementList)
  
  @_('FUN ID LPAREN RPAREN varList statementList')
  def funcMain(self, p):
    return Function(p.ID, [], p.varList, p.statementList)
  
  @_('statement SEMICOLON statementList')
  def statementList(self, p):
    return [p.statement] + p.statementList

  @_('statement')
  def statementList(self, p):
    return [p.statement]

  @_('WHILE relation DO statement')
  def statement(self, p):
    return DualStmt(p.WHILE, p.relation, p.DO, p.statement)

  @_('IF relation THEN statement')
  def statement(self, p):
    return DualStmt(p.IF, p.relation, p.THEN, p.statement)

  @_('IF relation THEN statement ELSE statement')
  def statement(self, p):
    return TripleStmt(p.IF, p.relation, p.THEN, p[3], p.ELSE, p[5])

  @_('ID ASSIGN expr')
  def statement(self, p):
    return Assign(p.ID, p.expr)

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

  @_('SKIP')
  def statement(self, p):
    return Single(p.SKIP)

  @_('BREAK')
  def statement(self, p):
    return Single(p.BREAK)

  @_('BEGIN statementList END')
  def statement(self, p):
    return Grouping(p.BEGIN, p.statementList, p.END)

  @_('expr LTE expr')
  def relation(self, p):
    return Relation(p.LTE, p[0], p[2])
  
  @_('expr LT expr')
  def relation(self, p):
    return Relation(p.LT, p[0], p[2])
  
  @_('expr GTE expr')
  def relation(self, p):
    return Relation(p.GTE, p[0], p[2])
  
  @_('expr GT expr')
  def relation(self, p):
    return Relation(p.GT, p[0], p[2])
  
  @_('expr EQ expr')
  def relation(self, p):
    return Relation(p.EQ, p[0], p[2])
  
  @_('expr NEQ expr')
  def relation(self, p):
    return Relation(p.NEQ, p[0], p[2])
  
  @_('relation AND relation')
  def relation(self, p):
    return Relation(p.AND, p[0], p[2])
  
  @_('relation OR relation')
  def relation(self, p):
    return Relation(p.OR, p[0], p[2])
  
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

  @_('expr PLUS expr')
  def expr(self, p):
    return Binary(p.PLUS, p[0], p[2])
  
  @_('expr MINUS expr')
  def expr(self, p):
    return Binary(p.MINUS, p[0], p[2])
  
  @_('expr TIMES expr')
  def expr(self, p):
    return Binary(p.TIMES, p[0], p[2])
  
  @_('expr DIVIDE expr')
  def expr(self, p):
    return Binary(p.DIVIDE, p[0], p[2])
  
  @_('MINUS expr')
  def expr(self, p):
    return Unary(p.MINUS, p.expr)
  
  @_('PLUS expr')
  def expr(self, p):
    return Unary(p.PLUS, p.expr)
  
  @_('LPAREN expr RPAREN')
  def expr(self, p):
    return p.expr
  
  @_('ID LPAREN exprList RPAREN')
  def expr(self, p):
    return Call(p.ID, p.exprList)
  
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
    return p.expr
  
  @_('TFLOAT LPAREN expr RPAREN')
  def expr(self, p):
    return p.expr
  
  @_('var COMMA argList')
  def argList(self, p):
    return [p.var] + p.argList

  @_('var')
  def argList(self, p):
    return [p.var]
  
  @_('var varList')
  def varList(self, p):
    return [p.var] + p.varList
  
  @_('var')
  def varList(self, p):
    return [p.var]

  @_('ID COLON TINT SEMICOLON')
  def var(self, p):
    return Var(p.ID, p.TINT)
  
  @_('ID COLON TFLOAT SEMICOLON')
  def var(self, p):
    return Var(p.ID, p.TFLOAT)
  
  @_('ID COLON TINT LBRACKET INT RBRACKET SEMICOLON')
  def var(self, p):
    return VectorVar(p.ID, p.TINT, p.INT)
  
  @_('ID COLON TFLOAT LBRACKET INT RBRACKET SEMICOLON')
  def var(self, p):
    return VectorVar(p.ID, p.TFLOAT, p.INT)
  
  @_('INT')
  def number(self, p):
    return Integer(p.INT)
  
  @_('FLOAT')
  def number(self, p):
    return Float(p.FLOAT)
  
  @_('MINUS INT')
  def number(self, p):
    n = -1 * p.INT
    return Integer(n)
  
  @_('MINUS FLOAT')
  def number(self, p):
    n = -1 * p.FLOAT
    return Float(n)
  
  @_('ID')
  def location(self, p):
    return Ident(p.ID)
  
  @_('ID LBRACKET INT RBRACKET')
  def location(self, p):
    return Vector(p.ID, p.INT)
  
  @_('ID LBRACKET ID RBRACKET')
  def location(self, p):
    return Vector(p[0], p[2])
  
  def error(self, p):
    if p:
      print("Syntax error at token", p.type,"line", p.lineno, "value", p.value)
      # Just discard the token and tell the parser it's okay.
      self.errok()
    else:
      print("Syntax error at EOF")
  
if __name__ == '__main__':
  lexer = LexerForPL0()
  parser = parserForPL0()
  with open('test.pl0', 'r') as f:
    text_input = f.read()
    print(text_input)
    print_lexer(text_input)
    result = parser.parse(lexer.tokenize(text_input))
    rprint(result)