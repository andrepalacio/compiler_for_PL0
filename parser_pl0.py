import logging
from sly import Parser
from lexer_pl0 import LexerForPL0
from model_ast import *

class parserForPL0(Parser):
  log = logging.getLogger()
  log.setLevel(logging.ERROR)
  expected_shift_reduce = 1
  debugfile = 'parser.out'

  tokens = LexerForPL0.tokens

  # grammar rules implementation

  @_('func* funcMain')
  def program(self, p):
    funcList = p.func.append(p.funcMain)
    return Program(funcList)
  
  @_('FUN ID LPAREN RPAREN LBRACE argList RBRACE var* BEGIN statementList END')
  def func(self, p):
    return Function(p.ID, p.argList, p.var, p.statementList)
  
  @_('FUN "main" LPAREN RPAREN LBRACE RBRACE var* BEGIN statementList END')
  def funcMain(self, p):
    return Function("main", [], p.var, p.statementList)
  
  @_('statement (SEMICOLON statementList)?')
  def statementList(self, p):
    stmtList = p.statementList.append(p.statement)
    return StatementList(stmtList)

  @_('WHILE relation DO statement')
  def statement(self, p):
    return DualStatement(p.WHILE, p.relation, p.DO, p.statement)

  @_('IF relation THEN statement')
  def statement(self, p):
    return DualStatement(p.IF, p.relation, p.THEN, p.statement)

  @_('IF relation THEN statement ELSE statement')
  def statement(self, p):
    return TripleStatement(p.IF, p.relation, p.THEN, p[3], p.ELSE, p[5])

  @_('ID ASSIGN expr')
  def statement(self, p):
    return Assign(p.ID, p.expr)

  @_('PRINT LPAREN STRING RPAREN')
  def statement(self, p):
    return OneStatement(p.PRINT, p.STRING)

  @_('WRITE LPAREN expr RPAREN')
  def statement(self, p):
    return OneStatement(p.WRITE, p.expr)

  @_('READ LPAREN LOCATION RPAREN')
  def statement(self, p):
    return OneStatement(p.READ, p.LOCATION)

  @_('RETURN expr')
  def statement(self, p):
    return OneStatement(p.RETURN, p.expr)

  @_('NAME LPAREN exprList RPAREN')
  def statement(self, p):
    return OneStatement(p.NAME, p.exprList)

  @_('SKIP')
  def statement(self, p):
    return Single(p.SKIP)

  @_('BREAK')
  def statement(self, p):
    return Single(p.BREAK)

  @_('BEGIN statementList END')
  def statement(self, p):
    return Join(p.BEGIN, p.statementList, p.END)

  @_('expr LT expr')
  def relation(self, p):
    return Relation(p.LT, p[0], p[1])
  
  @_('expr LE expr')
  def relation(self, p):
    return Relation(p.LE, p[0], p[1])
  
  @_('expr GT expr')
  def relation(self, p):
    return Relation(p.GT, p[0], p[1])
  
  @_('expr GE expr')
  def relation(self, p):
    return Relation(p.GE, p[0], p[1])
  
  @_('expr EQ expr')
  def relation(self, p):
    return Relation(p.EQ, p[0], p[1])
  
  @_('expr NE expr')
  def relation(self, p):
    return Relation(p.NE, p[0], p[1])
  
  @_('relation AND relation')
  def relation(self, p):
    return Relation(p.AND, p[0], p[1])
  
  @_('relation OR relation')
  def relation(self, p):
    return Relation(p.OR, p[0], p[1])
  
  @_('NOT relation')
  def relation(self, p):
    return Not(p.NOT, p.relation)
  
  @_('LPAREN relation RPAREN')
  def relation(self, p):
    return p.relation

  @_('expr (COMMA exprList)?')
  def exprList(self, p):
    exprList = p.exprList.append(p.expr)
    return ExprList(exprList)

  @_('expr PLUS expr')
  def expr(self, p):
    return Binary(p.PLUS, p[0], p[1])
  
  @_('expr MINUS expr')
  def expr(self, p):
    return Binary(p.MINUS, p[0], p[1])
  
  @_('expr TIMES expr')
  def expr(self, p):
    return Binary(p.TIMES, p[0], p[1])
  
  @_('expr DIVIDE expr')
  def expr(self, p):
    return Binary(p.DIVIDE, p[0], p[1])
  
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

  @_('var (COMMA argList)?')
  def argList(self, p):
    return p.argList
  
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
  
