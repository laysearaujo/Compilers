from lexer import *
import sys

def main(): 
    if len(sys.argv) != 2:
        sys.exit("Erro: Precisamos de um arquivo como argumento.")
    with open(sys.argv[1], 'r') as inputFile:
        input = inputFile.read()
    lexer = Lexer(input)
    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(str(token.kind) + " ("+ token.text +")")
        token = lexer.getToken()
     
main()