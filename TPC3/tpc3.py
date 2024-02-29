import re

def somar_numeros(texto):

    soma = 0
    continuar = True  # Inicia com a soma ativada

    # Processa cada segmento do texto
    for segmento in re.finditer(r'\d+|[a-zA-Z]+|=', texto):
        texto_segmento = segmento.group()

        # Verifica se o segmento contém 'on' ou 'off'
        if 'on' in texto_segmento.lower():
            continuar = True
        elif 'off' in texto_segmento.lower():
            continuar = False

        # Se estiver somando, adiciona qualquer número encontrado ao total
        if continuar and texto_segmento.isdigit():
            soma += int(texto_segmento)

        # Ao encontrar '=', imprime a soma atual e a reseta
        if texto_segmento == '=':
            print(soma)

# Exemplo de uso
texto = "1iMRE7r=HtzkAon8o2sdXVtM0oLoffzNxZi4t5eqOpZNEqCJaLonK1mMTy3d22WoffaJ8uH6sgDxy2xMJoNRQZ7aAmkmhF4N91eTqqzequb4eYpA34DIojequZtnvw6LyrPxme0eqZbYZPon82fFbYKoffQXTonOnjjAAzS4=eq1tKe0VQuS89yuoffLoNCs8rV24P3Eeq1GeAtonjvTK0A5KmKAEaOon1=deqQcZrZ5MBu58HzkequWQ5XC9Fon83ctoffFHaEQFtN9aIonfjAq9eqW0L6F9W4=eq=2pOQRUgAM56DKoffZ6BYeq7sYononKZV=eq0K9KdW=VononAid6Uon6GeoffW=onD=OffonEQ=offG=39MoNyOn=EQOff7offOn5DSOffOn9OnW=43Uk=OffOnON"
somar_numeros(texto)