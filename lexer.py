from sly import Lexer

class LexerForPL0(Lexer):

  # tokens
  tokens = [
    FUN, BEGIN, END, IF, THEN, ELSE, WHILE, DO, VAR, ASSIGN, PRINT, 
    READ, WRITE, RETURN, PLUS, MINUS, TIMES, DIVIDE, EQ, NEQ, LT, GT,
    LTE, GTE, SKIP, BREAK, AND, OR, NOT, INT, FLOAT, NUMBER, ID, STRING 
  ]

  #literals
  literals = { '(', ')', '{', '}', ';', ',' }

  # ignore spaces and tabs
  ignore = ' \t'

  # ignore comments
  ignore_comment = r'/\*.*\*/'

  # count newlines
  @_(r'\n+')
  def ignore_newline(self, t):
    self.lineno += t.value.count('\n')

  # error handling
  def error(self, t):
    print(f'Illegal character {t.value[0]}')
    self.index += 1

  #tokens declaration
  FUN = r'fun'
  BEGIN = r'begin'
  END = r'end'
  IF = r'if'
  THEN = r'then'
  ELSE = r'else'
  WHILE = r'while'
  DO = r'do'
  VAR = r':'
  ASSIGN = r':='
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
  INT = r'int'
  FLOAT = r'float'
  STRING = r'".*"'

  NUMBER = r'\d+|\d+.\d+'

  # ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
  ID = r'[a-zA-Z_]'

if __name__ == '__main__':
  lexer = LexerForPL0()
  text = '''
    fun main()
    v:int[8192];
    i:int;
    n:int;
  begin
    print("Entre n: ");
    read(n);
    i := 0;
    while i < n do
    begin
      read(v[i]);
      i := i+1
    end;
    quicksort(0, n-1, v);
    i := 0;
    while i < n-1 do
    begin
      write(v[i]); print(" ");
      if 0 < v[i] - v[i+1] then
      begin
        print("Quicksort falló "); write(i); print("\n") ; return(0)
      end
      else
        i := i+1
    end;
    write(v[i]);
    print("Éxito\n")
  end
  '''
  for tok in lexer.tokenize(text):
    print(tok)
