from Compiler.Lexer import Lexer
from Compiler.Scope import Scope
from Compiler.Parser import Parser
from Compiler.Evaluator import Evaluator
def EvaluateFunction(function,x,y):
   scope = Scope()
   scope.values = {"x": x,"y" : y}
   evaluator = Evaluator(scope)
   value = evaluator.Evaluate(function,scope)
   return value