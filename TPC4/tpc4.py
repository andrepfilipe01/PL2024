import sys
import re

tokens = [
    ('SELECT', r'SELECT'),
    ('FROM', r'FROM'),
    ('WHERE', r'WHERE'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('NUMBER', r'\d+'),
    ('COMMA', r','),
    ('OPERATOR', r'[><=!]+'),
    ('WHITESPACE', r'\s+')
]

# Função para gerar tokens a partir do código fonte
def lexer(code):
    position = 0
    while position < len(code):
        match = None
        for token_type, regex_pattern in tokens:
            pattern = re.compile(regex_pattern)
            match = pattern.match(code, position)
            if match:
                value = match.group(0)
                if token_type != 'WHITESPACE':
                    yield token_type, value
                position = match.end()
                break
        if not match:
            raise SyntaxError('Invalid character: ' + code[position])
    yield 'EOF', ''

# Função para testar o analisador léxico
def main():
    query = "SELECT id, nome, salario FROM empregados WHERE salario >= 820"
    for token in lexer(query):
        print(token)

if __name__ == "__main__":
    main()
