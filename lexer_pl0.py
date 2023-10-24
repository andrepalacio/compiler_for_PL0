from sly import Lexer
from rich.table import Table
from rich.console import Console
from sys import argv, exit
from json import loads

class LexerForPL0(Lexer):

  # tokens
  tokens = {
    FUN, BEGIN, END, IF, THEN, ELSE, WHILE, DO, COLON, ASSIGN, PRINT, READ, WRITE, RETURN,
    PLUS, MINUS, TIMES, DIVIDE, EQ, NEQ, LT, GT, LTE, GTE, SKIP, BREAK, AND, OR, NOT, 
    TINT, TFLOAT, INT, FLOAT, ID, STRING, LPAREN, RPAREN, SEMICOLON,
    COMMA, LBRACKET, RBRACKET,
  }

  # ignore spaces and tabs
  ignore = ' \t\r'

  # uncompleted comment
  @_(r'/\*.*[\s\S]*(?!\*/)')
  def uncompleted_comment(self, t):
    print(f'Uncompleted comment {t.value[0:5]} at line {t.lineno}')
    self.index += 1

  # integer
  @_(r'(([1-9]\d*)|0)(?![^\s,;\)\]])')
  def INT(self, t):
    t.value = int(t.value)
    return t

  # float number
  @_(r'(0|[1-9]\d*)(\.\d+)?(\d[e][+-]?\d+)?(?![^\s,;\)])')
  def FLOAT(self, t):
    if '.' in t.value:
      if 'e' not in t.value:
        t.value = float(t.value)
    return t

  # string
  STRING = r'"(?:\\["n\\]|[^"\\])+"'
  def STRING(self, t):
    t.value = loads(t.value)
    return t

  #tokens declaration
  FUN = r'fun\b'
  BEGIN = r'begin\b'
  END = r'end\b'
  IF = r'if\b'
  THEN = r'then\b'
  ELSE = r'else\b'
  WHILE = r'while\b'
  DO = r'do\b'
  PRINT = r'print\b'
  READ = r'read\b'
  WRITE = r'write\b'
  RETURN = r'return\b'
  SKIP = r'skip\b'
  BREAK = r'break\b'
  AND = r'and\b'
  OR = r'or\b'
  NOT = r'not\b'
  TINT = r'int\b'
  TFLOAT = r'float\b'
  ASSIGN = r':='
  COLON = r':'
  EQ = r'=='
  NEQ = r'!='
  LTE = r'<='
  LT = r'<'
  GTE = r'>='
  GT = r'>'
  PLUS = r'\+'
  MINUS = r'-'
  TIMES = r'\*'
  DIVIDE = r'/'
  LPAREN = r'\('
  RPAREN = r'\)'
  SEMICOLON = r';'
  COMMA = r','
  LBRACKET = r'\['
  RBRACKET = r'\]'

  # identifier
  ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

  # ignore comments
  @_(r'/\*[\s\S]*?\*/')
  def COMMENT(self, t):
    self.lineno += t.value.count('\n')
    return t


  # count newlines
  @_(r'\n+')
  def ignore_newline(self, t):
    self.lineno += t.value.count('\n')

  # error handling
  @_(r'[^\s]+')
  def error(self, t):
    print(f'Illegal character {t.value[0:5]}  at line {t.lineno}')
    next = self.index
    if self.text[next:next+1] == '\n':
      self.lineno += 1
    self.index += 1
    #self.lineno += 1

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
  if table.row_count == 0:
    console.print('\nNO TOKENS FOUND\n')
  else:
    console.print(table)
  

if __name__ == '__main__':
  if len(argv) != 2:
    print('Usage: python lexer.py <file>')
    exit(1)

  try:
    filePath = argv[1]
    with open(filePath) as f:
      text = f.read()
    print_lexer(text)
  except FileNotFoundError:
    print(f'File {filePath} not found')
    exit(1)
  except Exception as e:
    print(f'Error {e} occurred while reading file {filePath}')
    exit(1)
