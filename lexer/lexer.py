# -*- coding: utf-8 -*-
import enum
import sys

class Lexer:
    def __init__(self, input):
        self.source = input + '\n' #código-fonte (entrada)
        self.curChar = '' #caractere atual dentro do código-fonte
        self.curPos = -1
        self.nextChar()
        pass

    # Processa o proximo caractere
    def nextChar(self):
        self.curPos = self.curPos + 1
        if self.curPos >= len(self.source):
            self.curChar = '\0' #EOF
        else:
            self.curChar = self.source[self.curPos]

    # Retorna o caractere seguinte (ainda não lido).
    def peek(self):
        if self.curPos+1 >= len(self.source):
            return '\0'
        else: 
            return self.source[self.curPos+1]

    # Token inválido encontrado, método usado para imprimir mensagem de erro e encerrar.
    def abort(self, message):
        sys.exit("Erro léxico! " + message)
		
    # Pular espaço em branco
    def skipWhitespace(self):
        while self.curChar.isspace():
         self.nextChar()
		
    # Pular comentários.
    def skipComment(self):
        if self.curChar == '/':
            if self.peek() == '/':
                # Comentário de linha, pula até o final da linha
                while self.curChar != '\n':
                    self.nextChar()
                self.nextChar()
            elif self.peek() == '*':
                # Comentário de múltiplas linhas, pula até encontrar "*/"
                self.nextChar()  # Pula o primeiro *

                while True:
                    if self.curChar == '*' and self.peek() == '/':
                        self.nextChar()  # Pula o *
                        self.nextChar()  # Pula o /
                        break
                    elif self.curChar == '\0':
                        self.abort("Comentário de múltiplas linhas não foi fechado corretamente.")
                    else:
                        self.nextChar()
    
    def parseNumber(self):
        start_pos = self.curPos
        while self.curChar.isdigit():
            self.nextChar()

        numStr = self.source[start_pos:self.curPos]
        return Token(numStr, TokenType.NUMBER)

    def parseIdentifier(self):
        identStr = ""

        while self.curChar.isalnum() or self.curChar == '_':
            identStr += self.curChar
            self.nextChar()

        if identStr == "System":
            if self.curChar == '.' and self.peek() == 'o' and self.peek() == 'u' and self.peek() == 't' and self.peek() == '.' and self.peek() == 'p' and self.peek() == 'r' and self.peek() == 'i' and self.peek() == 'n' and self.peek() == 't' and not self.peek().isalnum() and self.peek() != '_':
                self.nextChar()  # Avança para '.'
                identStr += self.curChar
                self.nextChar()  # Avança para 'o'
                identStr += self.curChar
                self.nextChar()  # Avança para 'u'
                identStr += self.curChar
                self.nextChar()  # Avança para 't'
                identStr += self.curChar
                self.nextChar()  # Avança para '.'

                self.nextChar()  # Avança para 'p'
                identStr += self.curChar
                self.nextChar()  # Avança para 'r'
                identStr += self.curChar
                self.nextChar()  # Avança para 'i'
                identStr += self.curChar
                self.nextChar()  # Avança para 'n'
                identStr += self.curChar
                self.nextChar()  # Avança para 't'
                identStr += self.curChar
                self.nextChar()  # Avança para 'l'
                identStr += self.curChar
                self.nextChar()  # Avança para 'n'
                identStr += self.curChar
                self.nextChar()  # Avança para 't'
                identStr += self.curChar
                self.nextChar()  # Avança para '\n'

                return Token(identStr, TokenType.SYSTEM_OUT_PRINTLN)

        keyword = Token.checkIfKeyword(identStr)
        if keyword is not None:
            return Token(identStr, keyword)
        else:
            return Token(identStr, TokenType.IDENT)

    def parseSymbol(self):
        symbol = self.curChar
        tokenType = None

        if symbol == '&':
            if self.peek() == '&':
                symbol += self.peek()
                tokenType = TokenType.AND
                self.nextChar()
            else:
                tokenType = TokenType.UNKNOWN
        elif symbol == '<':
            tokenType = TokenType.LT
        elif symbol == '=':
            if self.peek() == '=':
                symbol += self.peek()
                tokenType = TokenType.EQEQ
                self.nextChar()
            else:
                tokenType = TokenType.EQ
        elif symbol == '!':
            if self.peek() == '=':
                symbol += self.peek()
                tokenType = TokenType.NOTEQ
                self.nextChar()
            else:
                tokenType = TokenType.NOT
        elif symbol == '+':
            tokenType = TokenType.PLUS
        elif symbol == '-':
            tokenType = TokenType.MINUS
        elif symbol == '*':
            tokenType = TokenType.MULT
        elif symbol == ';':
            tokenType = TokenType.SEMICOLON
        elif symbol == '.':
            tokenType = TokenType.DOT
        elif symbol == ',':
            tokenType = TokenType.COMMA
        elif symbol == '(':
            tokenType = TokenType.L_PAREN
        elif symbol == ')':
            tokenType = TokenType.R_PAREN
        elif symbol == '{':
            tokenType = TokenType.L_BRACK
        elif symbol == '}':
            tokenType = TokenType.R_BRACK
        elif symbol == '[':
            tokenType = TokenType.L_SQBRACK
        elif symbol == ']':
            tokenType = TokenType.R_SQBRACK
        else:
            tokenType = TokenType.UNKNOWN

        return Token(symbol, tokenType)                    
    # Return o próximo token --> Implementar esta função e as funções de skip acima 
    # Atualmente esta função retorna um token de tipo TEST para cada caractere do programa até alcançar EOF
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()

        while self.curChar != '\0':
            if self.curChar.isdigit():
                return self.parseNumber()
            elif self.curChar.isalpha() or self.curChar == '_':
                return self.parseIdentifier()
            else:
                token = self.parseSymbol()
                self.nextChar()
                if token is not None:
                    return token

        return Token(self.curChar, TokenType.EOF)
            
    
    
class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText #lexema, a instância específica encontrada
        self.kind = tokenKind # o tipo de token (TokenType) classificado
    
    @staticmethod
    def checkIfKeyword(word):
        if word == "System.out.println":
            return TokenType.SYSTEM_OUT_PRINTLN
        for kind in TokenType:
            if kind.name == word.upper() and kind.value > 100 and kind.value < 200:
                return kind
        return None

class TokenType(enum.Enum):
    EOF = -1
    TEST = 0 # token inutilizado, só para rodar 'sem erro'
    NUMBER = 1 #NUMERO
    IDENT = 2 #IDENTIFICADOR    
    #PALAVRAS RESERVADAS
    BOOLEAN = 101
    CLASS = 102
    PUBLIC = 103
    EXTENDS = 104
    STATIC = 105
    VOID = 106
    MAIN = 107
    STRING = 108
    INT = 109
    WHILE = 110
    IF = 111
    ELSE = 112
    RETURN = 113
    LENGTH = 114
    TRUE = 115
    FALSE = 116
    THIS = 117
    NEW = 118
    SYSTEM_OUT_PRINTLN = 119
    #OPERADORES
    AND = 201   # &&
    LT = 202    # <
    EQEQ = 203  # ==
    NOTEQ = 204 # !=
    PLUS = 205  # +
    MINUS = 206 # -
    MULT = 207  # *
    NOT = 208   # !
    #DELIMITADORES
    SEMICOLON = 251   # ;
    DOT = 252    # .
    COMMA = 253  # ,
    EQ = 254 # =
    L_PAREN = 255  # (
    R_PAREN = 256  # )
    L_BRACK = 257  # {
    R_BRACK = 258  # }
    L_SQBRACK = 259  # [
    R_SQBRACK = 260  # ]
    UNKNOWN = 261 # desconhecido