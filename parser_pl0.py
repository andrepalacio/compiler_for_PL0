import logging
from sly import Parser
from lexer_pl0 import LexerForPL0

class parserForPL0(Parser):
  log = logging.getLogger()
  log.setLevel(logging.ERROR)
  expected_shift_reduce = 1
  debugfile = 'parser.out'

  tokens = LexerForPL0.tokens

  # grammar rules implementation

  @_('func* funcMain')
  def program(self, p):
    return p.funcMain
  
  @_('FUN ID LPAREN RPAREN LBRACE argList RBRACE var* BEGIN statementList END')
  def func(self, p):
    return p.func
  
  @_('FUN "main" LPAREN RPAREN LBRACE RBRACE var* BEGIN statementList END')
  def funcMain(self, p):
    return p.funcMain
  
  @_('statement (SEMICOLON statementList)?')
  def statementList(self, p):
    return p.statementList

  @_('WHILE relation DO statement')
  def statement(self, p):
    return p.statement

  @_('IF relation THEN statement')
  def statement(self, p):
    return p.statement

  @_('IF relation THEN statement ELSE statement')
  def statement(self, p):
    return p.statement

  @_('NAME ASSIGN expr')
  def statement(self, p):
    return p.statement

  @_('PRINT LPAREN STRING RPAREN')
  def statement(self, p):
    return p.statement

  @_('WRITE LPAREN expr RPAREN')
  def statement(self, p):
    return p.statement

  @_('READ LPAREN LOCATION RPAREN')
  def statement(self, p):
    return p.statement

  @_('RETURN expr')
  def statement(self, p):
    return p.statement

  @_('NAME LPAREN exprList RPAREN')
  def statement(self, p):
    return p.statement

  @_('SKIP')
  def statement(self, p):
    return p.SKIP

  @_('BREAK')
  def statement(self, p):
    return p.BREAK

  @_('BEGIN statementList END')
  def statement(self, p):
    return p.statement

  '''
  relation ::= expr '<' expr
    | expr '<=' expr
    | expr '>' expr
    | expr '>=' expr
    | expr '==' expr
    | expr '!=' expr
    | relation 'and' relation
    | relation 'or' relation
    | 'not' relation
    | '(' relation ')'
  '''

  @_('expr LT expr')
  def relation(self, p):
    return p.expr
  
  @_('expr LE expr')
  def relation(self, p):
    return p.expr
  
  @_('expr GT expr')
  def relation(self, p):
    return p.expr
  
  @_('expr GE expr')
  def relation(self, p):
    return p.expr
  
  @_('expr EQ expr')
  def relation(self, p):
    return p.expr
  
  @_('expr NE expr')
  def relation(self, p):
    return p.expr
  
  @_('relation AND relation')
  def relation(self, p):
    return p.relation
  
  @_('relation OR relation')
  def relation(self, p):
    return p.relation
  
  @_('NOT relation')
  def relation(self, p):
    return p.relation
  
  @_('LPAREN relation RPAREN')
  def relation(self, p):
    return p.relation

  @_('expr (COMMA exprList)?')
  def exprList(self, p):
    return p.exprList

  @_('expr PLUS expr')
  def expr(self, p):
    return p.expr
  
  @_('expr MINUS expr')
  def expr(self, p):
    return p.expr
  
  @_('expr TIMES expr')
  def expr(self, p):
    return p.expr
  
  @_('expr DIVIDE expr')
  def expr(self, p):
    return p.expr
  
  @_('MINUS expr')
  def expr(self, p):
    return p.expr
  
  @_('PLUS expr')
  def expr(self, p):
    return p.expr
  
  @_('LPAREN expr RPAREN')
  def expr(self, p):
    return p.expr
  
  @_('ID LPAREN exprList RPAREN')
  def expr(self, p):
    return p.expr
  
  @_('ID')
  def expr(self, p):
    return p.ID
  
  @_('ID LBRACKET expr RBRACKET')
  def expr(self, p):
    return p.expr
  
  @_('number')
  def expr(self, p):
    return p.number
  
  @_('TINT LPAREN expr RPAREN')
  def expr(self, p):
    return p.expr
  
  @_('TFLOAT LPAREN expr RPAREN')
  def expr(self, p):
    return p.expr

  @_('arg (COMMA argList)?')
  def argList(self, p):
    return p.argList

  @_('ID COLON TINT')
  def arg(self, p):
    return p.arg
  
  @_('ID COLON TFLOAT')
  def arg(self, p):
    return p.arg
  
  @_('ID COLON TINT LBRACKET INT RBRACKET')
  def arg(self, p):
    return p.arg
  
  @_('ID COLON TFLOAT LBRACKET INT RBRACKET')
  def arg(self, p):
    return p.arg
  
  @_('ID COLON TINT SEMICOLON')
  def var(self, p):
    return p.var
  
  @_('ID COLON TFLOAT SEMICOLON')
  def var(self, p):
    return p.var
  
  @_('ID COLON TINT LBRACKET INT RBRACKET SEMICOLON')
  def var(self, p):
    return p.var
  
  @_('ID COLON TFLOAT LBRACKET INT RBRACKET SEMICOLON')
  def var(self, p):
    return p.var
  
  @_('INT')
  def number(self, p):
    return p.INT
  
  @_('FLOAT')
  def number(self, p):
    return p.FLOAT
  
  @_('MINUS INT')
  def number(self, p):
    return p.INT
  
  @_('MINUS FLOAT')
  def number(self, p):
    return p.FLOAT
  
  @_('ID')
  def location(self, p):
    return p.ID
  
  @_('ID LBRACKET INT RBRACKET')
  def location(self, p):
    return p.location
  
