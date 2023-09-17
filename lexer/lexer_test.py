from lexer import *
import sys

def testBinarySearch(): 
    file = "data/BinarySearch.java"
    with open(file, 'r') as inputFile:
        input = inputFile.read()
    lexer = Lexer(input)
    token = lexer.getToken()
    tokens = []
    tokens.append(token)
    while token.kind != TokenType.EOF:
        token = lexer.getToken()
        tokens.append(token)
    
    assert 650 == len(tokens)
    assert TokenType.IDENT == tokens[321].kind
    assert TokenType.L_PAREN == tokens[172].kind
    assert TokenType.IDENT == tokens[415].kind
    assert TokenType.COMMA == tokens[459].kind
    assert TokenType.IDENT == tokens[450].kind
    assert TokenType.SEMICOLON == tokens[508].kind
    assert TokenType.IDENT == tokens[215].kind
    assert TokenType.NUMBER == tokens[128].kind
    assert TokenType.EQ == tokens[269].kind
    assert TokenType.SEMICOLON == tokens[569].kind
    assert TokenType.SEMICOLON == tokens[204].kind
    assert TokenType.IDENT == tokens[95].kind
    assert TokenType.NUMBER == tokens[440].kind
    assert TokenType.IDENT == tokens[272].kind
    assert TokenType.EQ == tokens[487].kind
    assert TokenType.IDENT == tokens[595].kind
    assert TokenType.IDENT == tokens[531].kind
    assert TokenType.L_PAREN == tokens[196].kind
    assert TokenType.ELSE == tokens[225].kind
    assert TokenType.L_BRACK == tokens[566].kind

def testBinaryTree(): 
    file = "data/BinaryTree.java"
    with open(file, 'r') as inputFile:
        input = inputFile.read()
    lexer = Lexer(input)
    token = lexer.getToken()
    tokens = []
    tokens.append(token)
    while token.kind != TokenType.EOF:
        token = lexer.getToken()
        tokens.append(token)
    
    assert 1351 == len(tokens)
    assert TokenType.IDENT == tokens[330].kind
    assert TokenType.IDENT == tokens[217].kind
    assert TokenType.EQ == tokens[129].kind
    assert TokenType.IDENT == tokens[1163].kind
    assert TokenType.EOF == tokens[1350].kind
    assert TokenType.R_BRACK == tokens[1239].kind
    assert TokenType.R_BRACK == tokens[943].kind
    assert TokenType.R_BRACK == tokens[1348].kind
    assert TokenType.IDENT == tokens[527].kind
    assert TokenType.R_PAREN == tokens[529].kind
    assert TokenType.IDENT == tokens[712].kind
    assert TokenType.L_PAREN == tokens[159].kind
    assert TokenType.R_PAREN == tokens[763].kind
    assert TokenType.L_PAREN == tokens[939].kind
    assert TokenType.L_PAREN == tokens[1039].kind
    assert TokenType.TRUE == tokens[1343].kind
    assert TokenType.IDENT == tokens[1304].kind
    assert TokenType.IDENT == tokens[1284].kind
    assert TokenType.R_PAREN == tokens[1067].kind
    assert TokenType.R_PAREN == tokens[953].kind

def testBubbleSort(): 
    file = "data/BubbleSort.java"
    with open(file, 'r') as inputFile:
        input = inputFile.read()
    lexer = Lexer(input)
    token = lexer.getToken()
    tokens = []
    tokens.append(token)
    while token.kind != TokenType.EOF:
        token = lexer.getToken()
        tokens.append(token)
    
    assert 378 == len(tokens)
    assert TokenType.IDENT == tokens[11].kind
    assert TokenType.SEMICOLON == tokens[148].kind
    assert TokenType.EQ == tokens[362].kind
    assert TokenType.IDENT == tokens[207].kind
    assert TokenType.IDENT == tokens[358].kind
    assert TokenType.IDENT == tokens[232].kind
    assert TokenType.EQ == tokens[74].kind
    assert TokenType.EQ == tokens[369].kind
    assert TokenType.IDENT == tokens[225].kind
    assert TokenType.ELSE == tokens[218].kind
    assert TokenType.LT == tokens[152].kind
    assert TokenType.IDENT == tokens[112].kind
    assert TokenType.NUMBER == tokens[363].kind
    assert TokenType.R_PAREN == tokens[245].kind
    assert TokenType.PUBLIC == tokens[241].kind
    assert TokenType.L_PAREN == tokens[69].kind
    assert TokenType.INT == tokens[108].kind
    assert TokenType.SEMICOLON == tokens[308].kind
    assert TokenType.DOT == tokens[54].kind
    assert TokenType.L_BRACK == tokens[98].kind

def testLinearSearch(): 
    file = "data/LinearSearch.java"
    with open(file, 'r') as inputFile:
        input = inputFile.read()
    lexer = Lexer(input)
    token = lexer.getToken()
    tokens = []
    tokens.append(token)
    while token.kind != TokenType.EOF:
        token = lexer.getToken()
        tokens.append(token)
    
    assert 362 == len(tokens)
    assert TokenType.IDENT == tokens[268].kind
    assert TokenType.R_BRACK == tokens[266].kind
    assert TokenType.SEMICOLON == tokens[312].kind
    assert TokenType.SEMICOLON == tokens[186].kind
    assert TokenType.R_PAREN == tokens[124].kind
    assert TokenType.R_BRACK == tokens[259].kind
    assert TokenType.IDENT == tokens[334].kind
    assert TokenType.SEMICOLON == tokens[183].kind
    assert TokenType.NUMBER == tokens[311].kind
    assert TokenType.SEMICOLON == tokens[265].kind
    assert TokenType.SEMICOLON == tokens[85].kind
    assert TokenType.SEMICOLON == tokens[214].kind
    assert TokenType.SEMICOLON == tokens[290].kind
    assert TokenType.IDENT == tokens[185].kind
    assert TokenType.L_PAREN == tokens[235].kind
    assert TokenType.R_PAREN == tokens[206].kind
    assert TokenType.STATIC == tokens[4].kind
    assert TokenType.R_PAREN == tokens[12].kind
    assert TokenType.R_PAREN == tokens[113].kind
    assert TokenType.CLASS == tokens[29].kind

def testLinkedList(): 
    file = "data/LinkedList.java"
    with open(file, 'r') as inputFile:
        input = inputFile.read()
    lexer = Lexer(input)
    token = lexer.getToken()
    tokens = []
    tokens.append(token)
    while token.kind != TokenType.EOF:
        token = lexer.getToken()
        tokens.append(token)
    
    assert 1111 == len(tokens)
    assert TokenType.NUMBER == tokens[445].kind
    assert TokenType.R_PAREN == tokens[404].kind
    assert TokenType.PUBLIC == tokens[705].kind
    assert TokenType.BOOLEAN == tokens[290].kind
    assert TokenType.IDENT == tokens[745].kind
    assert TokenType.IDENT == tokens[915].kind
    assert TokenType.EQ == tokens[171].kind
    assert TokenType.NUMBER == tokens[1032].kind
    assert TokenType.BOOLEAN == tokens[383].kind
    assert TokenType.SEMICOLON == tokens[191].kind
    assert TokenType.IDENT == tokens[249].kind
    assert TokenType.COMMA == tokens[953].kind
    assert TokenType.R_PAREN == tokens[94].kind
    assert TokenType.IDENT == tokens[45].kind
    assert TokenType.IDENT == tokens[856].kind
    assert TokenType.R_BRACK == tokens[215].kind
    assert TokenType.SEMICOLON == tokens[357].kind
    assert TokenType.IDENT == tokens[799].kind
    assert TokenType.EQ == tokens[892].kind
    assert TokenType.R_PAREN == tokens[763].kind

def testQuickSort(): 
    file = "data/QuickSort.java"
    with open(file, 'r') as inputFile:
        input = inputFile.read()
    lexer = Lexer(input)
    token = lexer.getToken()
    tokens = []
    tokens.append(token)
    while token.kind != TokenType.EOF:
        token = lexer.getToken()
        tokens.append(token)
    
    assert 500 == len(tokens)
    assert TokenType.INT == tokens[408].kind
    assert TokenType.SEMICOLON == tokens[236].kind
    assert TokenType.SEMICOLON == tokens[486].kind
    assert TokenType.L_SQBRACK == tokens[269].kind
    assert TokenType.EQ == tokens[296].kind
    assert TokenType.NOT == tokens[239].kind
    assert TokenType.SEMICOLON == tokens[130].kind
    assert TokenType.IDENT == tokens[325].kind
    assert TokenType.IDENT == tokens[387].kind
    assert TokenType.NUMBER == tokens[357].kind
    assert TokenType.IDENT == tokens[346].kind
    assert TokenType.NUMBER == tokens[471].kind
    assert TokenType.L_SQBRACK == tokens[425].kind
    assert TokenType.EQ == tokens[166].kind
    assert TokenType.IDENT == tokens[282].kind
    assert TokenType.R_BRACK == tokens[403].kind
    assert TokenType.PUBLIC == tokens[3].kind
    assert TokenType.SEMICOLON == tokens[115].kind
    assert TokenType.IDENT == tokens[278].kind
    assert TokenType.TRUE == tokens[217].kind