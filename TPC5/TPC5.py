
import ply.lex as lex
import re
import sys

tokens =(
    'LEVANTAR', 'POUSAR',
    'MOEDA', 'T' ,'ABORTAR'
)

def t_LEVANTAR(t):
    r'(?i:LEVANTAR)'
    t.lexer.semaforo = True
    print("maq: \"Introduza moedas.\"")

def t_POUSAR(t):
    r'(?i:POUSAR)'
    t.lexer.semaforo = False
    print("maq: \"Volte sempre!\"")

def t_MOEDA(t):
    r'10c|20c|50c|1e|2e'
    if t.lexer.semaforo :
        if re.match( r'.+c',t.value):
            t.lexer.dinheiro += (int(re.search(r'\d+', str(t.value)).group()) * 0.01)
        else:
            t.lexer.dinheiro += int(re.search(r'\d+', str(t.value)).group())

def t_T(t):
    r'\d{9}$'
    if t.lexer.semaforo : 
        if re.match(r'^(800)\d{6}', t.value):
            t.lexer.numero = str(t.value)
        elif re.match(r'^(808)\d{6}', t.value): 
            if t.lexer.dinheiro >= 0.1:
                t.lexer.numero = str(t.value)
            else:
                print(f'Retorno do dinheiro: {int(t.lexer.dinheiro - t.lexer.dinheiro % 1)}e{int((t.lexer.dinheiro % 1) * 10)}c')
                t.lexer.numero = 0
        elif re.match(r'^(2)\d{8}', t.value):
            if t.lexer.dinheiro >= 0.25:
                t.lexer.numero = str(t.value)
            else:
                print(f'Retorno do dinheiro: {int(t.lexer.dinheiro - t.lexer.dinheiro % 1)}e{int((t.lexer.dinheiro % 1) * 10)}c')
                t.lexer.numero = 0
        elif re.match(r'', t.value):
            if t.lexer.dinheiro >= 1.5:
                t.lexer.numero = str(t.value)
            else:
                print(f'Retorno do dinheiro: {int(t.lexer.dinheiro - t.lexer.dinheiro % 1)}e{int((t.lexer.dinheiro % 1) * 10)}c')
                t.lexer.numero = 0
        elif re.match(r'^(?!(601|641))\d{9}', t.value):
            t.lexer.numero = str(t.value)
        else:
            print("maq: \"Esse número não é permitido neste telefone. Queira discar novo número!\"")
        print(t.lexer.dinheiro)

def t_ABORTAR(t):
    r'(?i:ABORTAR)'
    t.lexer.semaforo = False


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

lexer.semaforo = False
lexer.dinheiro = 0
lexer.numero = ""

for linha in sys.stdin:
    lexer.input(linha)
    for tok in lexer:
        print(tok)
    if not lexer.semaforo:
        break

# 
# Falta Fazer:
#   Executavel;
#   Devolver Troco;
# 
# #