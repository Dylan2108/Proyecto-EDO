from Compiler.Expression import Expression
from Compiler.Scope import Scope
class Evaluator:
    def __init__(self,scope):
        self.scope = scope
    def Evaluate(self,expression : Expression,scope : Scope):
        return expression.Evaluate(scope)