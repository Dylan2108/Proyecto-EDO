from enum import Enum
class TokenType(Enum):
    # Keywords
    LeftParenthesis = 1
    RightParenthesis = 2
    Plus = 3
    Less = 4
    Multiply = 5
    Divide = 6
    Pow = 7
    Variable = 8
    SenFunction = 9
    CosFunction = 10
    Numbers = 11
    EOF = 12
class Token:
    def __init__(self,value,type,literal):
        self.value = value
        self.type = type
        self.literal = literal