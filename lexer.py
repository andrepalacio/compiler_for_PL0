from sly import Lexer
from rich.table import Table
from rich.console import Console

class LexerForPL0(Lexer):

  # tokens
  tokens = [
    FUN, BEGIN, END, IF, THEN, ELSE, WHILE, DO, VARDECL, ASSIGN, PRINT, 
    READ, WRITE, RETURN, PLUS, MINUS, TIMES, DIVIDE, EQ, NEQ, LT, GT,
    LTE, GTE, SKIP, BREAK, AND, OR, NOT, TINT, TFLOAT, NUMBER, INT, ID, LITERAL
  ]

  #literals
  literals = { '(', ')', '{', '}', ';', ',', '[', ']'}

  # ignore spaces and tabs
  ignore = ' \t\r'

  # ignore comments
  ignore_comment = r'/\*.*\*/'

  # integer
  @_(r'\d+')
  def INT(self, t):
    t.value = int(t.value)
    return t

  # float or int number
  @_(r'-?(\d+|\d+.\d+)')
  def NUMBER(self, t):
    if '.' in t.value:
      t.value = float(t.value)
    else:
      t.value = int(t.value)
    return t

  #tokens declaration
  FUN = r'fun'
  BEGIN = r'begin'
  END = r'end'
  IF = r'if'
  THEN = r'then'
  ELSE = r'else'
  WHILE = r'while'
  DO = r'do'
  ASSIGN = r':='
  VARDECL = r':'
  PRINT = r'print'
  READ = r'read'
  WRITE = r'write'
  RETURN = r'return'
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
  SKIP = r'skip'
  BREAK = r'break'
  AND = r'and'
  OR = r'or'
  NOT = r'not'
  TINT = r'int'
  TFLOAT = r'float'
  
  # string literal
  LITERAL = r'"(?:[^"\\]|\\["n\\])*"'

  # identifier
  ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

  # count newlines
  @_(r'\n+')
  def ignore_newline(self, t):
    self.lineno += t.value.count('\n')

  # uncompleted comment
  @_(r'/\*.*')
  def ignore_uncompleted_comment(self, t):
    print(f'Uncompleted comment at line {self.lineno}')
    self.index += 1

  # error handling
  def error(self, t):
    print(f'Illegal character {t.value[0]} at line {self.lineno}')
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
