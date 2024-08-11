"""
Gramática Forth


Compiler -> Prog

Prog -> Prog Inst
    | ε

Inst -> NUM
    | OP
    | Function
    | String_Exp
    | Variables
    | Conditional
    | Cicle
    | Maneuvers

           
Function -> : NAME Prog ;
        | NAME

String_Exp -> .
            | STRING
            | EMIT
            | CHAR
            | CR
            | KEY
            | SPACE
            | SPACES

Conditional -> IF Prog ELSE Prog THEN
            | IF Prog THEN

Cicle -> DO Prog LOOP
        | I
        | BEGIN Prog UNTIL
  
OP ->  +
    | -
    | *
    | /
    | >
    | <
    | = 
    | NOT_EQUAL
    | GREATER_EQUAL
    | LESS_EQUAL
    | MOD
    | MOD2
    | NEGATE
    | MAX
    | MIN

Maneuvers -> SWAP
          | DUP
          | OVER
          | DROP
          | 2DUP
          | 2SWAP
          | 2DROP

Variables -> VARIABLE NAME
          | NAME !
          | NAME @
          | NAME ?

"""


import ply.lex as lex

tokens = ('NUM', 
          'NAME',
          'COMMENT',
          'VARIABLE',
          'MOD','MOD2','NOT_EQUAL', 'GREATER_EQUAL', 'LESS_EQUAL','MAX', 'MIN' , 'NEGATE', 
          'STRING','CHAR','EMIT','CR','KEY','SPACE','SPACES',
          'IF','THEN','ELSE',
          'DO','LOOP','I', 'BEGIN', 'UNTIL',
          'SWAP', 'DUP', 'OVER', 'ROT', 'DROP', '2SWAP', '2DUP', '2OVER', '2DROP'
          )
literals = "+-*/:;!@,<>.=?"

t_ignore = ' \t\n\r'



def t_COMMENT(t):
    r'\(.*\)'
    pass

def t_VARIABLE(t):
    r'\b[vV][aA][rR][iI][aA][bB][lL][eE]\b'
    return t

def t_MOD2(t):
    r'\/MOD\b'
    return t


def t_MOD(t):
    r'\b[Mm][Oo][Dd]\b'
    return t


def t_NOT_EQUAL(t):
    r'<>'
    return t

def t_GREATER_EQUAL(t):
    r'>='
    return t

def t_LESS_EQUAL(t):
    r'<='
    return t

def t_MAX(t):
    r'\b[Mm][Aa][Xx]\b'
    return t

def t_MIN(t):
    r'\b[Mm][Ii][Nn]\b'
    return t

def t_NEGATE(t):
    r'\b[Nn][Ee][Gg][Aa][Tt][Ee]\b'
    return t

def t_STRING(t):
    r'\." .*?"'
    t.value = '"' + t.value[3:]
    return t

def t_CHAR(t):
    r'\b[cC][hH][aA][rR]\s+\S+'  
    t.value = t.value.split()[1][0]
    return t



def t_EMIT(t):
    r'\b[eE][mM][iI][tT]\b'
    return t

def t_CR(t):
    r'\b[cC][rR]\b'
    return t

def t_KEY(t):
    r'\b[kK][eE][yY]\b'
    return t

def t_SPACE(t):
    r'\b[sS][pP][aA][cC][eE]\b'
    return t

def t_SPACES(t):
    r'\b[sS][pP][aA][cC][eE][sS]\b'
    return t

def t_IF(t):
    r'\b[iI][fF]\b'
    return t

def t_THEN(t):
    r'\b[tT][hH][eE][nN]\b'
    return t

def t_ELSE(t):
    r'\b[eE][lL][sS][eE]\b'
    return t

def t_DO(t):
    r'\b[dD][oO]\b'
    return t

def t_LOOP(t):
    r'\b[lL][oO][oO][pP]\b'
    return t

def t_I(t):
    r'\b[iI]\b'
    return t

def t_BEGIN(t):
    r'\b[bB][eE][gG][iI][nN]\b'
    return t

def t_UNTIL(t):
    r'\b[uU][nN][tT][iI][lL]\b'
    return t


def t_SWAP(t):
    r'\b[sS][wW][aA][pP]\b'
    return t

def t_DUP(t):
    r'\b[dD][uU][pP]\b'
    return t

def t_OVER(t):
    r'\b[oO][vV][eE][rR]\b'
    return t

def t_ROT(t):
    r'\b[rR][oO][tT]\b'
    return t

def t_DROP(t):
    r'\b[dD][rR][oO][pP]\b'
    return t

def t_2SWAP(t):
    r'\b[2][sS][wW][aA][pP]\b'
    return t

def t_2DUP(t):
    r'\b[2][dD][uU][pP]\b'
    return t

def t_2OVER(t):
    r'\b[2][oO][vV][eE][rR]\b'
    return t

def t_2DROP(t):
    r'\b[2][dD][rR][oO][pP]\b'
    return t


def t_NUM(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_NAME(t):
    r'[_a-zA-Z][_a-zA-Z0-9.?\-]*'
    return t




def t_error(t):
    print(f'Illegal character: {t.value[0]}')
    t.lexer.skip(1)



lexer = lex.lex()