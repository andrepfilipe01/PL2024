import ply.yacc as yacc
from calculo_lex import tokens

# Definição da pilha
stack = []

# Regras de análise sintática
def p_statement(p):
    """
    statement : expression
              | statement expression
    """

def p_expression(p):
    """
    expression : expression expression operator
               | NUMBER
    """
    if len(p) == 2:
        stack.append(float(p[1]))
    elif p[3] == '+':
        stack[-2] = stack[-2] + stack[-1]
        stack.pop()
    elif p[3] == '-':
        stack[-2] = stack[-2] - stack[-1]
        stack.pop()
    elif p[3] == '*':
        stack[-2] = stack[-2] * stack[-1]
        stack.pop()
    elif p[3] == '/':
        stack[-2] = stack[-2] / stack[-1]
        stack.pop()

def p_operator(p):
    """
    operator : PLUS
             | MINUS
             | TIMES
             | DIVIDE
    """
    p[0] = p[1]

def p_error(p):
    print("Syntax error in input!")

# Construir o parser
parser = yacc.yacc()

# Função para testar o parser
def test_parser(input_string):
    # Limpar a pilha antes de testar uma nova expressão
    stack.clear()
    # Parse da entrada
    parser.parse(input_string)
    return stack  # Retorne a pilha inteira em vez do último elemento
    # Limpar a pilha antes de testar uma nova expressão
    stack.clear()
    # Parse da entrada
    parser.parse(input_string)
    return stack  # Retorne a pilha inteira em vez do último elemento
