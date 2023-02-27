
import sys

semaforo = True
soma = 0

def check_string_for_number(linha):
    r = 0
    for c in linha:
        if c.isdigit():
            r = (r*10) + int(c)
    return r

for linha in sys.stdin:
    number = check_string_for_number(linha)
    if linha.casefold().find("on") != -1:
        semaforo = True
    if linha.casefold().find("off") != -1:
        semaforo = False
    if number != 0 and semaforo:
        soma += number
    if linha.find("=") != -1:
        print(soma) 
