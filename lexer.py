from sly import Lexer
from rich.table import Table
from rich.console import Console

class LexerForPL0(Lexer):

  # tokens
  tokens = [
    FUN, BEGIN, END, IF, THEN, ELSE, WHILE, DO, VARDECL, ASSIGN, PRINT, 
    READ, WRITE, RETURN, PLUS, MINUS, TIMES, DIVIDE, EQ, NEQ, LT, GT,
    LTE, GTE, SKIP, BREAK, AND, OR, NOT, TINT, TFLOAT, INT, FLOAT, ID, STRING
  ]

  #literals
  literals = { '(', ')', '{', '}', ';', ',', '[', ']'}

  # ignore spaces and tabs
  ignore = ' \t\r'

  # ignore comments
  ignore_comment = r'/\*.*\*/'

  # float number
  @_(r'((([1-9]\d*)|0)(\.\d+(e[+-]?\d+)?))|((([1-9]\d*)|0)e[+-]?\d+)')
  def FLOAT(self, t):
    if '.' in t.value:
      if 'e' not in t.value:
        t.value = float(t.value)
    return t
  
  # integer
  @_(r'(([1-9]\d+)|0)(?![\de-])')
  def INT(self, t):
    t.value = int(t.value)
    return t

  # string
  STRING = r'"(?:[^"\\]|\\["n\\])*"'

  # identifier
  ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

  #tokens declaration
  ID['fun'] = FUN
  ID['begin'] = BEGIN
  ID['end'] = END
  ID['if'] = IF
  ID['then'] = THEN
  ID['else'] = ELSE
  ID['while'] = WHILE
  ID['do'] = DO
  ID[':='] = ASSIGN
  ID[':'] = VARDECL
  ID['print'] = PRINT
  ID['read'] = READ
  ID['write'] = WRITE
  ID['return'] = RETURN
  ID['skip'] = SKIP
  ID['break'] = BREAK
  ID['and'] = AND
  ID['or'] = OR
  ID['not'] = NOT
  ID['int'] = TINT
  ID['float'] = TFLOAT
  PLUS = r'\+'
  MINUS = r'-'
  TIMES = r'\*'
  DIVIDE = r'/'
  EQ = r'=='
  NEQ = r'!='
  LT = r'<'
  GT = r'>'
  LTE = r'<='
  GTE = r'>='

  # count newlines
  @_(r'\n+')
  def ignore_newline(self, t):
    self.lineno += t.value.count('\n')

  # uncompleted comment
  @_(r'/\*.*')
  def ignore_uncompleted_comment(self, t):
    print(f'Uncompleted comment at line {t.lineno}')
    self.index += 1

  # error handling
  @_(r'.+')
  def error(self, t):
    print(f'Illegal character {t.value} at line {t.lineno}')
    self.lineno += 1
    self.index += 1

def print_lexer(source):
  #print tokens using rich library
  lexer = LexerForPL0()
  console = Console()
  table = Table(title='Tokens')
  table.add_column('Type')
  table.add_column('Value')
  table.add_column('Line', justify='right')
  table.add_column('Index', justify='right')
  table.add_column('End', justify='right')
  for tok in lexer.tokenize(source):
    table.add_row(tok.type, str(tok.value), str(tok.lineno), str(tok.index), str(tok.end))
  console.print(table)
  

if __name__ == '__main__':
  filePath = './test1/badnumbers.pl0'
  with open(filePath) as f:
    text = f.read()
  print_lexer(text)
