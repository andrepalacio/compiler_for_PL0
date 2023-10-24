from sly import Parser
from rich import print as rprint
from lexer_pl0 import LexerForPL0, print_lexer
from model_ast import *

class parserForPL0(Parser):
  #expected_shift_reduce = 1
  debugfile = 'parserPL0.txt'

  precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
  )

  tokens = LexerForPL0.tokens

  # grammar rules implementation
  
  @_('func funcList')
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
  def func(self, p):
    return Function(p.ID, [], p.varList, p.statementList)
  
  @_('statements SEMICOLON statementList')
  def statementList(self, p):
    return [p.statements] + p.statements
  
  @_('statements')
  def statementList(self, p):
    return [p.statements]
  
  @_('statement', 'noStatement')
  def statements(self, p):
    return [p[0]]

  @_('WHILE relation DO statement')
  def statement(self, p):
    return DualStmt(p.WHILE, p.relation, p.DO, p.statement)

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
  
  @_('IF relation THEN statement')
  def noStatement(self, p):
    return DualStmt(p.IF, p.relation, p.THEN, p.statement)

  @_('expr relExpr expr')
  def relation(self, p):
    return Relation(p[1], p[0], p[2])
  
  @_('LTE', 'LT', 'GTE', 'GT', 'EQ', 'NEQ', 'AND', 'OR')
  def relExpr(self, p):
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
    return Binary(p[0], p[0], p[2])
  
  @_('MINUS expr', 'PLUS expr')
  def expr(self, p):
    return Unary(p[0], p.expr)
  
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
  
  @_('varDecl COMMA argList')
  def argList(self, p):
    return [p.var] + p.argList

  @_('varDecl')
  def argList(self, p):
    return [p.var]
  
  @_('varDecl SEMICOLON varList', 'func SEMICOLON varList')
  def varList(self, p):
    return [p[0]] + p.varList
  
  @_('varDecl', 'func')
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
    return p[0]
  
  @_('TINT LBRACKET expr RBRACKET', 'TFLOAT LBRACKET expr RBRACKET')
  def vectorType(self, p):
    return p[0], p[2]

  @_('INT')
  def number(self, p):
    return Integer(p.INT)
  
  @_('FLOAT')
  def number(self, p):
    return Float(p.FLOAT)
  
  """ @_('MINUS INT')
  def number(self, p):
    n = -1 * p.INT
    return Integer(n)
  
  @_('MINUS FLOAT')
  def number(self, p):
    n = -1 * p.FLOAT
    return Float(n) """
  
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
    # if p:
    #   print("Syntax error at token", p.type,"line", p.lineno, "value", p.value)
    #   # Just discard the token and tell the parser it's okay.
    #   self.errok()
    # else:
    #   print("Syntax error at EOF")
    pass
  
if __name__ == '__main__':
  lexer = LexerForPL0()
  parser = parserForPL0()
  with open('test.pl0', 'r') as f:
    text_input = f.read()
    # print(text_input)
    # print_lexer(text_input)
    result = parser.parse(lexer.tokenize(text_input))
    # rprint(result)