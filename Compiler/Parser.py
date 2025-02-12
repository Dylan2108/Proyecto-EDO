from Compiler.Token import Token
from Compiler.Token import TokenType
from Compiler.Expression import SenFunction
from Compiler.Expression import CosFunction
from Compiler.Expression import NumberExpression
from Compiler.Expression import GroupingExpression
from Compiler.Expression import BinaryExpression
from Compiler.Expression import VariableExpression
from Compiler.Expression import NegativeFunction
class Parser:
    def __init__(self,tokens : []):
        self.tokens = tokens
        self.currentPosition = 0
    def Peek(self):
        return self.tokens[self.currentPosition]
    def Previous(self):
        return self.tokens[self.currentPosition - 1]
    def IsAtEnd(self):
        return self.Peek().type == TokenType.EOF
    def Advance(self):
        if(not self.IsAtEnd()):
            self.currentPosition += 1
        return self.Previous()
    def Check(self,type):
        if self.IsAtEnd():
            return False
        return self.Peek().type == type
    def Continue(self,type):
        if self.IsAtEnd():
            return False
        return self.tokens[self.currentPosition + 1].type == type
    def Consume(self,type):
        if self.Check(type):
            return self.Advance()
        raise Exception("Expresion inesperada")
    def Match(self,types):
        for type in types:
            if self.Check(type):
                self.Advance()
                return True
        return False
    def Expression(self):
        return self.ParseTerm()
    def ParseSen(self):
        self.Consume(TokenType.LeftParenthesis)
        expression = self.Expression()
        self.Consume(TokenType.RightParenthesis)
        return SenFunction(expression)
    def ParseCos(self):
        self.Consume(TokenType.LeftParenthesis)
        expression = self.Expression()
        return CosFunction(expression)
    def ParsePrimary(self):
        if self.Match([TokenType.SenFunction]):
            return self.ParseSen()
        if self.Match([TokenType.CosFunction]):
            return self.ParseCos()
        if self.Match([TokenType.Variable]):
            return VariableExpression(self.Previous().value)
        raise Exception("Expresion inesperada")
    def ParseLiteral(self):
        if self.Match([TokenType.Less]):
            expression = self.ParseLiteral()
            return NegativeFunction(expression)
        if self.Match([TokenType.Numbers]):
            return NumberExpression(float(self.Previous().value))
        if self.Match([TokenType.LeftParenthesis]):
            expression = self.Expression()
            self.Consume(TokenType.RightParenthesis)
            return GroupingExpression(expression)
        return self.ParsePrimary()
    def ParseFactor(self):
        expression = self.ParsePow()
        while self.Match([TokenType.Multiply,TokenType.Divide]):
            operator = self.Previous()
            right = self.ParsePow()
            expression = BinaryExpression(expression,operator,right)
        return expression
    def ParseTerm(self):
        expression = self.ParseFactor()
        if self.Check(TokenType.Plus) or self.Check(TokenType.Less):
            while self.Match([TokenType.Plus,TokenType.Less]):
                operator = self.Previous()
                right = self.ParseFactor()
                expression = BinaryExpression(expression,operator,right)
        return expression
    def ParsePow(self):
        expression = self.ParseLiteral()
        if self.Match([TokenType.Pow]):
            operator = self.Previous()
            right = self.ParseLiteral()
            return BinaryExpression(expression,operator,right)
        return expression