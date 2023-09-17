import enum
import sys

class SymbolType(enum.Enum):
    TERMINAL = 0
    NONTERMINAL = 1
    EPSILON = 2
    EOF = 3

class Symbol:
    def __init__(self,name,type):
        self.name = name
        self.type = type
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return self.name

class Nonterminal(Symbol):
    def __init__(self, name):
        super().__init__(name, SymbolType.NONTERMINAL)

class Terminal(Symbol):
    def __init__(self, name):
        super().__init__(name, SymbolType.TERMINAL)

class SpecialSymbol(Symbol):
    def __init__(self, name, type):
        if type == SymbolType.EPSILON or type == SymbolType.EOF: 
            super().__init__(name, type)
        else: 
            sys.exit('Tipo inválido')

EPSILON = SpecialSymbol('ε', SymbolType.EPSILON)
EOF = SpecialSymbol('$', SymbolType.EOF)

class Rule: 
    def __init__(self, nt, production):
        self.nonterminal = nt
        self.production = production
    def __str__(self):
        return str(self.nonterminal) + " -> " + ' '.join([str(e) for e in self.production])

class Grammar:
    def __init__(self, productions, startSymbol):
        self.productions = productions
        self.startSymbol = startSymbol
        self.nonTerminals = set()
        self.terminals = set()
        for p in productions:
            self.nonTerminals.add(p.nonterminal)
            for s in p.production:
                if isinstance(s,Terminal):
                    self.terminals.add(s)

        self.firstSet = {}
        self.followSet = {}
        self.parsingTable = {}
        self.buildFirstSets()
        self.buildFollowSets()
        self.generateParsingTable()


    def buildFirstSets(self):
        # Condição inicial dos conjuntos FIRST (incluindo definição de FIRST(t)=t onde t é um terminal, EOF, ou EPSILON)
        self.firstSet[EOF] = {EOF}
        self.firstSet[EPSILON] = {EPSILON}
        for t in self.terminals:
            self.firstSet[t] = {t}
        for nt in self.nonTerminals:
            self.firstSet[nt] = set()

        changed = True
        while changed:
            changed = False
            for rule in self.productions:
                nt = rule.nonterminal
                for symbol in rule.production:
                    if isinstance(symbol, Terminal):
                        # Se é um terminal, adiciona-o ao conjunto FIRST do não-terminal atual
                        if symbol not in self.firstSet[nt]:
                            self.firstSet[nt].add(symbol)
                            changed = True
                        break
                    elif isinstance(symbol, SpecialSymbol):
                        # Se é EPSILON ou EOF, o adiciona ao conjunto FIRST do não-terminal atual
                        if symbol not in self.firstSet[nt]:
                            self.firstSet[nt].add(symbol)
                            changed = True
                        break
                    else:
                        # Se é um não-terminal, faz a união dos conjuntos FIRST e considera EPSILON se necessário
                        for sym in self.firstSet[symbol]:
                            if sym != EPSILON and sym not in self.firstSet[nt]:
                                self.firstSet[nt].add(sym)
                                changed = True
                        if EPSILON not in self.firstSet[symbol]:
                            break


    def buildFollowSets(self):
        # Condição inicial dos conjuntos FOLLOW
        for nt in self.nonTerminals:
            self.followSet[nt] = set()
        self.followSet[self.startSymbol].add(EOF)

        changed = True
        while changed:
            changed = False
            for rule in self.productions:
                nonterminal = rule.nonterminal
                production = rule.production

                for i in range(len(production)):
                    symbol = production[i]
                    if isinstance(symbol, Nonterminal):
                        if i == len(production) - 1:
                            # se o símbolo for o último da produção, adicione o conjunto FOLLOW do não terminal
                            for follow_symbol in self.followSet[nonterminal]:
                                if follow_symbol not in self.followSet[symbol]:
                                    self.followSet[symbol].add(follow_symbol)
                                    changed = True
                        else:
                            next_symbol = production[i + 1]
                            if isinstance(next_symbol, Terminal):
                                # se o próximo símbolo for um terminal, adicione-o ao conjunto FOLLOW do símbolo atual
                                if next_symbol != EPSILON:
                                    if next_symbol not in self.followSet[symbol]:
                                        self.followSet[symbol].add(next_symbol)
                                        changed = True
                            else:
                                # Se o próximo símbolo for não terminal, adicione o PRIMEIRO conjunto do próximo símbolo
                                # excluindo EPSILON, para o conjunto FOLLOW do símbolo atual
                                for next_first in self.firstSet[next_symbol]:
                                    if next_first != EPSILON and next_first not in self.followSet[symbol]:
                                        self.followSet[symbol].add(next_first)
                                        changed = True
                                # Se o próximo símbolo pode produzir EPSILON, adicione o conjunto FOLLOW do não terminal
                                # excluindo EPSILON, para o conjunto FOLLOW do símbolo atual
                                if EPSILON in self.firstSet[next_symbol]:
                                    for follow_symbol in self.followSet[nonterminal]:
                                        if follow_symbol != EPSILON and follow_symbol not in self.followSet[symbol]:
                                            # tirando o $ quando não for a primeira gramatica
                                            if follow_symbol == EOF and isinstance(production[-1], Terminal):
                                                self.followSet[symbol].add(production[-1])
                                            else:
                                                self.followSet[symbol].add(follow_symbol)
                                                changed = True


    def generateParsingTable(self):
        # Estrutura da tabela
        for nt in self.nonTerminals:
            self.parsingTable[nt] = {}
            for t in self.terminals:
                self.parsingTable[nt][t.name] = []
            # Adicionando EOF como coluna
            self.parsingTable[nt]['$'] = []

        # Preencher a tabela de parsing com as regras de produção apropriadas
        for rule in self.productions:
            nt = rule.nonterminal
            for symbol in rule.production:
                if isinstance(symbol, Terminal):
                    self.parsingTable[nt][symbol.name].append(rule.production)
                    break
                elif isinstance(symbol, SpecialSymbol):
                    if symbol == EPSILON:
                        for follow_symbol in self.followSet[nt]:
                            self.parsingTable[nt][follow_symbol.name].append(rule.production)
                    break
                else:
                    for first_symbol in self.firstSet[symbol]:
                        if first_symbol != EPSILON:
                            self.parsingTable[nt][first_symbol.name].append(rule.production)
                    if EPSILON not in self.firstSet[symbol]:
                        break


    def checkIfLL1(self):
        for nt in self.nonTerminals:
            # Verificar se há conflitos na tabela de parsing para cada não-terminal
            for t in self.terminals:
                productions = self.parsingTable[nt][t.name]
                if len(productions) > 1:
                    return False
            # Verificar se há conflitos entre os conjuntos FIRST e FOLLOW para cada não-terminal
            for t in self.followSet[nt]:
                if t == EPSILON:
                    return False
        return True


    #Algoritmo de parsing, assume que cada caractere é um token 
    #NÃO É NECESSÁRIO MUDAR ESTE ALGORITMO
    def parse(self, sentence): 
        if not self.checkIfLL1():
            return 'Erro, gramática não é LL(1)!'
        else:
            size = len(sentence)
            i = 0
            stack = [EOF, self.startSymbol]
            a = sentence[i] 
            X = stack[len(stack)-1]
            while X != EOF:
                if type(X) == Terminal: 
                    if X.name == a: 
                        stack.pop()
                        i = i+1
                        if i < size:
                            a = sentence[i]
                        else: 
                            a = '$'
                    else:
                        return 'Erro sintático, esperava por '+X.name+' e apareceu '+a+'!'
                elif type(X) == Nonterminal:  
                    if len(self.parsingTable[X][a]) == 0:
                        return 'Erro sintático, caractere inesperado para resolver não-terminal '+X.name+': ' + a
                    elif len(self.parsingTable[X][a]) == 1:
                        stack.pop()
                        for s in reversed(self.parsingTable[X][a][0]):
                            if s != EPSILON:
                                stack.append(s)
                else:
                    return 'Tem algo errado com a tabela de parsing.'
                X = stack[len(stack)-1]
            if a == '$':
                return 'Palavra válida'
            else: 
                return 'Erro sintático, esperava por $ e apareceu: '+a