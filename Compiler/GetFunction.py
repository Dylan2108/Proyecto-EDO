from Compiler.Lexer import Lexer
from Compiler.Parser import Parser
def GetFunction(function):
    lexer = Lexer(function)
    tokens = lexer.GetTokens()
    parser = Parser(tokens)
    func = parser.Expression()
    return func