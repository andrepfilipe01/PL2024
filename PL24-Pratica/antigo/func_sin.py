import ply.yacc as yacc
from func import tokens

variables = {}

# Definição das regras de análise sintática
def p_S(p):
    """
    S : Exp DOLLAR
    """
    print("Resultado:", p[1])

def p_Exp(p):
    """
    Exp : Termo
        | Exp Termo PLUS
        | Exp Termo MINUS
        | Exp Termo TIMES
        | Exp Termo DIVIDE
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[3] == '+':
            p[0] = p[1] + p[2]
        elif p[3] == '-':
            p[0] = p[1] - p[2]
        elif p[3] == '*':
            p[0] = p[1] * p[2]
        elif p[3] == '/':
            p[0] = p[1] / p[2]

def p_Termo(p):
    """
    Termo : NUMBER
          | LPAR Exp RPAR
          | ID
    """
    if len(p) == 2:
        if isinstance(p[1], str):  # If the token is an identifier
            p[0] = variables.get(p[1], 0)  # Get its value from the dictionary or 0 if not found
        else:
            p[0] = p[1]
    else:
        p[0] = p[2]

# Tratamento de erro
def p_error(p):
    print("Erro de sintaxe!")

# Build the parser
parser = yacc.yacc()

# Testando o parser usando input
while True:
    try:
        s = input("calc > ")
    except EOFError:
        break
    parser.parse(s)
