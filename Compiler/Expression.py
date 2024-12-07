from Compiler.Scope import Scope
from abc import ABC,abstractmethod
from Compiler.Token import Token
from Compiler.Token import TokenType
import math
import numpy as np
class Expression(ABC):
    @abstractmethod
    def Evaluate(self,scope : Scope):
        pass
class NumberExpression(Expression):
    def __init__(self,value):
        self.value = value
    def Evaluate(self,scope : Scope):
        return self.value
class VariableExpression(Expression):
    def __init__(self,name):
        self.name = name
    def Evaluate(self,scope : Scope):
        return scope.values[self.name]
class BinaryExpression(Expression):
    def __init__(self,left : Expression, symbol : Token ,right : Expression):
        self.left = left
        self.symbol = symbol
        self.right = right
    def Evaluate(self, scope: Scope):
        left = self.left.Evaluate(scope)
        right = self.right.Evaluate(scope)
        if(self.symbol.type == TokenType.Plus):
            return left + right
        elif(self.symbol.type == TokenType.Less):
            return left - right
        elif (self.symbol.type == TokenType.Multiply):
            return left * right
        elif (self.symbol.type == TokenType.Divide):
            return left / right
        elif(self.symbol.type == TokenType.Pow):
            return left ** right
        else:
            raise Exception("Invalid operator")
class GroupingExpression(Expression):
    def __init__(self,expression : Expression):
        self.expression = expression
    def Evaluate(self, scope: Scope):
        return (self.expression.Evaluate(scope))
class SenFunction(Expression):
    def __init__(self,expression : Expression):
        self.expression = expression
    def Evaluate(self, scope: Scope):
        return np.sin(self.expression.Evaluate(scope))
class CosFunction(Expression):
    def __init__(self, expression : Expression):
        self.expression = expression
    def Evaluate(self, scope: Scope):
        return np.cos(self.expression.Evaluate(scope))