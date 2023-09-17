from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser

class ArithmeticVisitor:
    def __init__(self):
        self.variables = {}

    def visit(self, ctx):
        if isinstance(ctx, ArithmeticParser.ProgramContext):
            return self.visitProgram(ctx)
        elif isinstance(ctx, ArithmeticParser.StatementContext):
            return self.visitStatement(ctx)
        elif isinstance(ctx, ArithmeticParser.AssignmentContext):
            return self.visitAssignment(ctx)
        elif isinstance(ctx, ArithmeticParser.ExprContext):
            return self.visitExpr(ctx)
        elif isinstance(ctx, ArithmeticParser.TermContext):
            return self.visitTerm(ctx)
        elif isinstance(ctx, ArithmeticParser.FactorContext):
            return self.visitFactor(ctx)

    def visitProgram(self, ctx):
        result = None
        for statement in ctx.statement():
            result = self.visit(statement)
        return result

    def visitStatement(self, ctx):
        return self.visit(ctx.getChild(0))

    def visitAssignment(self, ctx):
        var_name = ctx.VAR().getText()
        value = self.visit(ctx.expr())
        self.variables[var_name] = value
        return value

    def visitExpr(self, ctx):
        result = self.visit(ctx.term(0))
        for i in range(1, len(ctx.term())):
            op = ctx.getChild(2 * i - 1).getText()
            if op == '+':
                result += self.visit(ctx.term(i))
            else:
                result -= self.visit(ctx.term(i))
        return result

    def visitTerm(self, ctx):
        result = self.visit(ctx.factor(0))
        for i in range(1, len(ctx.factor())):
            op = ctx.getChild(2 * i - 1).getText()
            if op == '*':
                result *= self.visit(ctx.factor(i))
            else:
                result /= self.visit(ctx.factor(i))
        return result

    def visitFactor(self, ctx):
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.VAR():
            var_name = ctx.VAR().getText()
            if var_name in self.variables:
                return self.variables[var_name]
            else:
                raise Exception("Variable not found: " + var_name)
        else:
            return self.visit(ctx.expr())

def main():
    visitor = ArithmeticVisitor()

    while True:
        expression = input("Digite uma expressão aritmética ou atribuição (ou 'exit' para sair): ")
        if expression == "exit":
            break

        lexer = ArithmeticLexer(InputStream(expression))
        stream = CommonTokenStream(lexer)
        parser = ArithmeticParser(stream)
        tree = parser.program()
        result = visitor.visit(tree)
        print("Resultado:", result)

if __name__ == '__main__':
    main()