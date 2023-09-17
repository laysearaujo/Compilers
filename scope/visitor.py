from symboltable import *
from exceptions import *

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class GenericVisitor(NodeVisitor):
    def __init__(self,tree):
        self.ast = tree

    def traverse(self):
        self.visit(self.ast)
    
    def erro(self,msg):
        raise Exception(msg)

    def undeclaredVariable(self,name):
        raise UndeclaredVariable(name)

    def alreadyDeclaredVariable(self,name):
        raise AlreadyDeclaredVariable(name)

    def varTypeMismatch(self,name, expected, actual):
        raise VarTypeMismatch(name, expected, actual)

    def booleanExpTypeMismatch(self, stmt, actual):
        raise BooleanExpTypeMismatch(stmt, actual)

    def arithExpTypeMismatch(self, left_type, right_type):
        raise ArithExpTypeMismatch(left_type, right_type)

    def relExpTypeMismatch(self, left_type, right_type):
        raise RelExpTypeMismatch(left_type, right_type)

    def visit_Program(self,node):
        for stmt in node.stmts:
            self.visit(stmt)
    def visit_LetStmt(self, node):
        self.visit(node.exp)
    def visit_VarDeclStmt(self,node):
        pass
    def visit_PrintStmt(self,node):
        self.visit(node.exp)
    def visit_InputStmt(self,node):
        pass
    def visit_BlockStmt(self,node):
        for stm in node.body: 
            self.visit(stm)
    def visit_WhileStmt(self,node):
        self.visit(node.cond)
        for stm in node.body: 
            self.visit(stm)
    def visit_IfStmt(self,node):
        self.visit(node.cond)
        for stm in node.body: 
            self.visit(stm)

    def visit_NumExpr(self, node):
        pass
    def visit_IdExpr(self,node):
        pass
    def visit_StringExpr(self, node):
        pass    
    def visit_GreaterThanExpr(self,node):
        self.visit(node.left)
        self.visit(node.right)
    def visit_GreaterThanEqualsExpr(self,node):
        self.visit(node.left)
        self.visit(node.right)
    def visit_LessThanExpr(self,node):
        self.visit(node.left)
        self.visit(node.right)
    def visit_LessThanEqualsExpr(self,node):
        self.visit(node.left)
        self.visit(node.right)
    def visit_EqualsExpr(self,node):
        self.visit(node.left)
        self.visit(node.right)
    def visit_NotEqualsExpr(self,node):
        self.visit(node.left)
        self.visit(node.right)
    def visit_UnaryPlusExpr(self,node):
        self.visit(node.exp)
    def visit_UnaryMinusExpr(self,node):
        self.visit(node.exp)    
    def visit_SumExpr(self,node):
        self.visit(node.left)
        self.visit(node.right)
    def visit_SubExpr(self,node):
        self.visit(node.left)
        self.visit(node.right)
    def visit_MulExpr(self,node):
        self.visit(node.left)
        self.visit(node.right)
    def visit_DivExpr(self,node):
        self.visit(node.left)
        self.visit(node.right)

        
class TypeCheckVisitor(GenericVisitor):
    def __init__(self, tree):
        super().__init__(tree)
        self.symbolTable = ScopedSymbolTable(scope_name="program", scope_level=1)

    def typecheck(self):
        # Inicia a análise de tipo percorrendo a árvore sintática
        self.traverse()

    def BOOLEAN(self):
        # Obtém a representação da tabela de símbolos para o tipo BOOLEAN
        return self.symbolTable.lookup("BOOLEAN")

    def INT(self):
        # Obtém a representação da tabela de símbolos para o tipo INT
        return self.symbolTable.lookup("INT")

    def STRING(self):
        # Obtém a representação da tabela de símbolos para o tipo STRING
        return self.symbolTable.lookup("STRING")

    def visit_InputStmt(self, node):
        # Verifica se a variável de entrada foi declarada
        variable_name = node.id
        symbol = self.symbolTable.lookup(variable_name)
        if symbol is None:
            self.undeclaredVariable(variable_name)

        return symbol

    def visit_LetStmt(self, node):
        # Verifica se a variável na declaração 'let' foi declarada
        id = node.id
        symbol = self.symbolTable.lookup(id)
        if symbol is None:
            raise UndeclaredVariable(id)

        # Verifica o tipo da expressão associada
        visit_type = self.visit(node.exp)
        if visit_type != symbol.type:
            raise VarTypeMismatch(id, symbol.type, visit_type)

    def visit_VarDeclStmt(self, node):
        # Verifica se a variável na declaração foi declarada no escopo atual
        variable_name = node.id
        symbol = self.symbolTable.lookup(variable_name, current_scope_only=True)

        if symbol is not None:
            self.alreadyDeclaredVariable(variable_name)

        # Insere a variável na tabela de símbolos
        symbol = Symbol(node.id, str(BuiltInTypeSymbol(node.type)))
        self.symbolTable.insert(variable_name, symbol)

    def visit_WhileStmt(self, node):
        # Verifica se a condição do loop while é do tipo BOOLEAN
        type = self.visit(node.cond)
        if type != str(self.BOOLEAN()):
            self.booleanExpTypeMismatch("WHILE", type)

    def visit_IfStmt(self, node):
        # Verifica se a condição do condicional if é do tipo BOOLEAN
        type = self.visit(node.cond)
        if type != str(self.BOOLEAN()):
            self.booleanExpTypeMismatch("IF", type)

    def visit_BlockStmt(self, node):
        # Cria um novo escopo para o bloco e visita suas declarações
        self.symbolTable = ScopedSymbolTable(
            scope_name=node.name,
            scope_level=self.symbolTable.scope_level + 1,
            enclosing_scope=self.symbolTable,
        )
        for stmt in node.body:
            self.visit(stmt)
        self.symbolTable = self.symbolTable.enclosing_scope

    def visit_NumExpr(self, node):
        # Expressão numérica sempre tem tipo INT
        return str(BuiltInTypeSymbol("INT"))

    def visit_StringExpr(self, node):
        # Expressão de string sempre tem tipo STRING
        return str(BuiltInTypeSymbol("STRING"))

    def visit_IdExpr(self, node):
        # Verifica se o identificador da expressão foi declarado
        symbol = self.symbolTable.lookup(node.id)
        if symbol is None:
            raise UndeclaredVariable(node.id)
        else:
            return symbol.type

    def visit_SumExpr(self, node):
        # Verifica se as expressões à esquerda e à direita do operador '+' são INT
        left = self.visit(node.left)
        right = self.visit(node.right)

        if left != str(self.INT()) or right != str(self.INT()):
            raise ArithExpTypeMismatch(left, right)
        return str(BuiltInTypeSymbol("INT"))

    def visit_DivExpr(self, node):
        # Verifica se as expressões à esquerda e à direita do operador '/' são INT
        left = self.visit(node.left)
        right = self.visit(node.right)

        if left != str(self.INT()) or right != str(self.INT()):
            raise ArithExpTypeMismatch(left, right)
        return str(BuiltInTypeSymbol("INT"))

    def visit_MulExpr(self, node):
        # Verifica se as expressões à esquerda e à direita do operador '*' são INT
        left = self.visit(node.left)
        right = self.visit(node.right)

        if left != str(self.INT()) or right != str(self.INT()):
            raise ArithExpTypeMismatch(left, right)
        return str(BuiltInTypeSymbol("INT"))

    def visit_GreaterThanExpr(self, node):
        # Verifica se as expressões à esquerda e à direita do operador '>' são INT
        left = self.visit(node.left)
        right = self.visit(node.right)

        if left != str(self.INT()) or right != str(self.INT()):
            raise TypeCheckError("Operador lógico requer um valor contável")
        return str(BuiltInTypeSymbol("BOOLEAN"))

    def visit_GreaterThanEqualsExpr(self, node):
        # Verifica se as expressões à esquerda e à direita do operador '>=' são INT
        left = self.visit(node.left)
        right = self.visit(node.right)

        if left != str(self.INT()) or right != str(self.INT()):
            raise TypeCheckError("Operador lógico requer um valor contável")
        return str(BuiltInTypeSymbol("BOOLEAN"))

    def visit_LessThanEqualsExpr(self, node):
        # Verifica se as expressões à esquerda e à direita do operador '<=' são INT
        left = self.visit(node.left)
        right = self.visit(node.right)

        if left != str(self.INT()) or right != str(self.INT()):
            raise TypeCheckError("Operador lógico requer um valor contável")
        return str(BuiltInTypeSymbol("BOOLEAN"))

    def visit_LessThanExpr(self, node):
        # Verifica se as expressões à esquerda e à direita do operador '<' são INT
        left = self.visit(node.left)
        right = self.visit(node.right)

        if left != str(self.INT()) or right != str(self.INT()):
            raise TypeCheckError("Operador lógico requer um valor contável")
        return str(BuiltInTypeSymbol("BOOLEAN"))

    def visit_EqualsExpr(self, node):
        # Verifica se as expressões à esquerda e à direita do operador '==' têm os mesmos tipos
        left = self.visit(node.left)
        right = self.visit(node.right)

        if left != right:
            raise TypeCheckError("Os tipos devem ser iguais")

        return str(BuiltInTypeSymbol("BOOLEAN"))

    def visit_NotEqualsExpr(self, node):
        # Verifica se as expressões à esquerda e à direita do operador '!=' têm tipos diferentes
        left = self.visit(node.left)
        right = self.visit(node.right)

        if left == right:
            raise TypeCheckError("Os tipos devem ser diferentes")
        
        return str(BuiltInTypeSymbol("BOOLEAN"))
