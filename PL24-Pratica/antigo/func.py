import ply.lex as lex

# List of token names
tokens = (
    'NUMBER',
    'LPAR',
    'RPAR',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'DOLLAR',
    'SEMICOLON',
    'COLON',
    'ID',
    'EXPRESSION',
)

# Regular expression rules for simple tokens
t_LPAR = r'\('
t_RPAR = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_SEMICOLON = r';'
t_COLON = r':'
t_DOLLAR = r'\$'

# Define a rule to recognize expressions
#def t_EXPRESSION(t):
#   r'[\+\-\*/\d\s]+'  # Operators, numbers, and whitespace for expression
#  return t

# Define a rule to recognize identifiers
def t_ID(t):
    r'[A-Z]+'
    t.type = 'ID'
    return t

# Define a rule to recognize floating-point numbers
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

# Define a rule to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Define a rule to ignore whitespace characters
t_ignore = ' \t'

# Define a rule for error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}, position {t.lexpos}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Take input from the terminal
expression = input("Enter an expression: ")

# Give the expression to the lexer
lexer.input(expression)

# Tokenize the expression
for token in lexer:
    print(token)
