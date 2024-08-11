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

import ply.yacc as yacc
from analex_forth import tokens, lexer, literals
import sys

var = {}
cicles = {}
maneuvers = {}
erros = []


func = {}
n_cond = 0
n_ciclo = 0
n_manuever = 0

def total_length():
    return len(var) + len(cicles) + len(maneuvers)


def p_Compiler(p): 
    "Compiler : Prog" 
    if 'CicleCountI' in p[1]:
        erros.append("Error: 'I' can only be used inside a loop.")
    else: 
        inicio = ""
        for _ in range(total_length()):
            inicio += 'pushi 0\n'
        p[0] = f'{inicio}START\n{p[1]}STOP\n'


def p_Prog1(p): "Prog : Prog Inst"; p[0] = p[1] + p[2]
def p_Prog2(p): "Prog : "; p[0] = ""

def p_Inst1(p): "Inst : NUM";  p[0] = f'pushi {p[1]}\n'
def p_Inst2(p): "Inst : OP";  p[0] = p[1]
def p_Inst3(p): "Inst : Function" ; p[0] = p[1]
def p_Inst4(p): "Inst : String_Exp"; p[0] = p[1]
def p_Inst5(p): "Inst : Variables"; p[0] = p[1]
def p_Inst6(p): "Inst : Conditional"; p[0] = p[1]
def p_Inst7(p): "Inst : Cicle"; p[0] = p[1]
def p_Inst8(p): "Inst : Maneuvers"; p[0] = p[1]
def p_Inst9(p): "Inst : COMMENT"; p[0] = ""

def p_OP1(p): "OP : '+'" ; p[0] = 'ADD\n'
def p_OP2(p): "OP : '-'" ; p[0] = 'SUB\n'
def p_OP3(p): "OP : '*'" ; p[0] = 'MUL\n'
def p_OP4(p): "OP : '/'" ; p[0] = 'DIV\n'
def p_OP5(p): "OP : MOD"  ; p[0] = 'MOD\n' 
def p_OP6(p): "OP : '>'" ; p[0] = 'SUP\n'
def p_OP7(p): "OP : '<'" ; p[0] = 'INF\n'
def p_OP8(p): "OP : '='" ; p[0] = 'EQUAL\n' 
def p_OP9(p): "OP : NOT_EQUAL" ; p[0] = 'EQUAL\nNOT\n'
def p_OP10(p): "OP : GREATER_EQUAL" ; p[0] = 'SUPEQ\n'
def p_OP11(p): "OP : LESS_EQUAL" ; p[0] = 'INFEQ\n'
def p_OP12(p): 
    "OP : MOD2"
    global n_manuever
    n_manuever += 1
    mod1 = f'MOD1{n_manuever}\n'
    maneuvers[mod1] = total_length()
    mod2 = f'MOD2{n_manuever}\n'
    maneuvers[mod2] = total_length()
    pos1 = maneuvers[mod1]
    pos2 = maneuvers[mod2]
    p[0] = f'storeg {pos1}\nstoreg {pos2}\npushg {pos2}\npushg {pos1}\nMOD\npushg {pos2}\npushg {pos1}\nDIV\n'

def p_OP14(p): "OP : NEGATE" ; p[0] = 'pushi -1\nMUL\n'
def p_OP15(p):
    "OP : MAX"
    global n_cond
    n_cond += 1
    dup_2 = f'pushsp\nload-1\npushsp\nload-1\n'
    p[0] = f'{dup_2}sup\njz ENDIF{n_cond}\npop 1\nENDIF{n_cond}\nSWAP\npop 1\n'
def p_OP16(p):
    "OP : MIN"
    global n_cond
    n_cond += 1
    dup_2 = f'pushsp\nload-1\npushsp\nload-1\n'
    p[0] = f'{dup_2}inf\njz ENDIF{n_cond}\npop 1\nENDIF{n_cond}\nSWAP\npop 1\n'


def p_Function1(p): 
    "Function : ':' NAME Prog ';'"
    if p[2] in func:
        erros.append(f'Error: Function {p[2]} is already defined.')
    else:
        func[p[2]] = p[3]
    p[0] = ""

def p_Function2(p): 
    "Function : NAME"
    if p[1] not in func:
        erros.append(f'Error: Function {p[1]} is not defined.')
        p[0] = ""
    elif p[1].lower() == "char":
        erros.append("Error: Argument missing for CHAR word.")
    else: p[0] = func[p[1]]


def p_String_Exp1(p): "String_Exp : '.'"; p[0] = 'WRITEI\n'
def p_String_Exp2(p): "String_Exp : STRING"; p[0] = f'pushs {p[1]}\nWRITES\n'
def p_String_Exp3(p): "String_Exp : EMIT"; p[0] = f'WRITECHR\n'
def p_String_Exp4(p): "String_Exp : CHAR"; p[0] = f'pushs "{p[1]}"\nCHRCODE\n'
def p_String_Exp5(p): "String_Exp : CR"; p[0] = 'WRITELN\n'
def p_String_Exp6(p): "String_Exp : KEY"; p[0] = 'READ\nATOI\n'
def p_String_Exp7(p): "String_Exp : SPACE"; p[0] = 'pushs " "\nWRITES\n'
def p_String_Exp8(p): 
    "String_Exp : SPACES"
    global n_ciclo
    n_ciclo+= 1
    ciclo = f'LOOP{n_ciclo}'
    cicles[f'limite_sup{ciclo}'] = total_length() # guardar o valor do limite superior
    cicles[f'limite_inf{ciclo}'] = total_length() # guardar o valor do limite inferior
    pos_sup = cicles[f'limite_sup{ciclo}']
    pos_inf = cicles[f'limite_inf{ciclo}']
    p[0] = f'pushi 0\nstoreg {pos_inf}\nstoreg {pos_sup}\nDo{ciclo}:\npushs " "\nWRITES\npushg {pos_inf}\npushi 1\nadd\ndup 1\nstoreg {pos_inf}\npushg {pos_sup}\nSUPEQ\njz Do{ciclo}\n'

def p_Variables1(p):
    "Variables : VARIABLE NAME"
    if p[2] in var:
        erros.append(f'Error: Variable {p[2]} is already defined.')
        return
    var[p[2]] = total_length()
    p[0] = ""

def p_Variables2(p):
    "Variables : NAME '!'"
    if p[1] not in var:
        erros.append(f'Error: Variable {p[1]} is not defined.')
    else:
        p[0] = f'storeg {var[p[1]]}\n'

def p_Variables3(p):
    "Variables : NAME '@'"
    if p[1] not in var:
        erros.append(f'Error: Variable {p[1]} is not defined.')
    else:
        p[0] = f'pushg {var[p[1]]}\n'
        
def p_Variables4(p):
    "Variables : NAME '?'"
    if p[1] not in var:
        erros.append(f'Error: Variable {p[1]} is not defined.')
    else:
        p[0] = f'pushg {var[p[1]]}\nwritei\n'

def p_Conditional1(p):
    "Conditional : IF Prog ELSE Prog THEN"
    global n_cond
    n_cond += 1
    p[0] = f"jz ELSE{n_cond}\n{p[2]}jump ENDIF{n_cond}\nELSE{n_cond}:\n{p[4]}ENDIF{n_cond}:\n"

def p_Conditional2(p):
    "Conditional : IF Prog THEN"
    global n_cond
    n_cond += 1
    p[0] = f"jz ENDIF{n_cond}\n{p[2]}ENDIF{n_cond}:\n"


def p_Cicle1(p):
    "Cicle : DO Prog LOOP"
    global n_ciclo
    n_ciclo+= 1
    ciclo = f'LOOP{n_ciclo}'
    cicles[f'limite_sup{ciclo}'] = total_length() # guardar o valor do limite superior
    cicles[f'limite_inf{ciclo}'] = total_length() # guardar o valor do limite inferior
    pos_sup = cicles[f'limite_sup{ciclo}']
    pos_inf = cicles[f'limite_inf{ciclo}']

    # Se tiver o counter i fazer pushg do limite inferior
    prog = p[2].replace("CicleCountI", f"pushg {pos_inf}")

    p[0] = f'storeg {pos_inf}\nstoreg {pos_sup}\nDo{ciclo}:\n{prog}pushg {pos_inf}\npushi 1\nadd\ndup 1\nstoreg {pos_inf}\npushg {pos_sup}\nSUPEQ\njz Do{ciclo}\n'

def p_Cicle2(p):
    "Cicle : I"
    p[0] = "CicleCountI\n"

def p_Cicle4(p):
    "Cicle : BEGIN Prog UNTIL"
    global n_ciclo
    n_ciclo += 1
    ciclo = f'LOOP{n_ciclo}'
    p[0] = f'BEGIN{ciclo}:\n{p[2]}jz BEGIN{ciclo}\n'



def p_Maneuvers1(p): "Maneuvers : SWAP"; p[0] = 'SWAP\n'
def p_Maneuvers2(p): "Maneuvers : DUP"; p[0] = 'DUP 1\n'
def p_Maneuvers3(p): "Maneuvers : OVER"; p[0] = 'pushsp\nload -1\n'
def p_Maneuvers4(p): 
    "Maneuvers : ROT"
    global n_manuever
    n_manuever +=1
    rot = f'ROT{n_manuever}'
    maneuvers[rot] = total_length() 
    pos_rot = maneuvers[rot] # posicao do ROT
    p[0] = f'storeg {pos_rot}\nSWAP\npushg {pos_rot}\nSWAP\n'

def p_Maneuvers5(p): "Maneuvers : DROP"; p[0] = 'pop 1\n'
def p_Maneuvers6(p): "Maneuvers : 2DUP"; p[0] = 'pushsp\nload-1\npushsp\nload-1\n'
def p_Maneuvers7(p): 
    "Maneuvers : 2SWAP"
    global n_manuever
    n_manuever += 1
    swap1 = f'SWAP1{n_manuever}'
    maneuvers[swap1] = total_length() # para guardar topo da stack
    swap2 = f'SWAP2{n_manuever}'
    maneuvers[swap2] = total_length() # para guardar segundo elemento da stack
    swap3 = f'SWAP3{n_manuever}'
    maneuvers[swap3] = total_length() # para guardar terceiro elemento da stack
    swap4 = f'SWAP4{n_manuever}'
    maneuvers[swap4] = total_length() # para guardar quarto elemento da stack
    pos_swap1 = maneuvers[swap1] # posicao do SWAP1
    pos_swap2 = maneuvers[swap2] # posicao do SWAP2
    pos_swap3 = maneuvers[swap3] # posicao do SWAP3
    pos_swap4 = maneuvers[swap4] # posicao do SWAP4
    p[0] = f'storeg {pos_swap1}\nstoreg {pos_swap2}\nstoreg {pos_swap3}\nstoreg {pos_swap4}\npushg {pos_swap2}\npushg {pos_swap1}\npushg {pos_swap4}\npushg {pos_swap3}\n'

def p_Maneuvers8(p): "Maneuvers : 2DROP"; p[0] = 'pop 1\npop 1\n'
def p_Maneuvers9(p): "Maneuvers : 2OVER"; p[0] = 'pushsp\nload -3\npushsp\nload -3\n'



def p_error(p):
    if p:
        erros.append(f"Syntax error at {p.value}")
    else:
        erros.append(f"Syntax error at EOF")


parser = yacc.yacc(debug=True)

def parse_stdin():
    data = sys.stdin.read()
    return parser.parse(data, lexer=lexer)

def main():
    result = parse_stdin()
    
    if erros:
        for erro in erros:
            print(erro)
    else:
        print(result)
        with open('output.txt', 'w') as f:
            print(result, file=f)

if __name__ == '__main__':
    main()