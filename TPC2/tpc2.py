import re

def cabecalho(texto):

    regex = r'^(#+)\s*(.*)$'

    # ^ inicio de linha
    # $ fim de linha
    # (#+) 1 ou mais
    # '\s*' zero ou mais e considera quaisquer espaços entre os caracteres # e o texto
    # '.*' corresponde a qualquer caractere

    modified_string = re.sub(regex,lambda match: f"<h{len(match.group(1))}>{match.group(2)}</h{len(match.group(1))}>" , texto, flags=re.MULTILINE)
    return modified_string

#def bold(texto):


#def italico(texto):

#def lista_numerada(texto):


def link(texto):
    return f"<a href='{texto}'></a>"
def imagem(texto):
    return f"<img src='{texto}'></img>"

markdown_text = """
# Exemplo de cabeçalho 
## Exemplo de cabeçalho 
### Exemplo de cabeçalho 
"""

html_output = cabecalho(markdown_text)
print(html_output)