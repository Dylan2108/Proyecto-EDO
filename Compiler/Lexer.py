from Compiler.Token import TokenType
from Compiler.Token import Token
class Lexer:
    def __init__(self,input : str):
        self.input = input
        self.tokens = []
        self.start = 0
        self.current = 0
        self.Keywords = {"sen" : Token("Sen",TokenType.SenFunction,"Sen"),"cos" : Token("Cos",TokenType.CosFunction,"Cos")}
    def IsAtEnd(self):
        #Verifica si ya se llego al final del texto
        return self.current >= len(self.input)
    def AddToken(self,type,literal):
        #Agrega el token con su respectivo valor a la lista
        text = self.input[self.start:self.current]
        self.tokens.append(Token(text,type,literal))
    def Advance(self):
        #Devuelve el caracter actual y avanza al siguiente
        self.current += 1
        return self.input[self.current - 1]
    def Match(self,expected):
        #Devuelve verdadero si el caracter actual coincide con el esperado
        if(self.IsAtEnd()):
            return False
        if(self.input[self.current] != expected):
            return False
        self.current += 1
        return True
    def Peek(self):
        #Devuelve el caracter actual y no avanza al siguiente
        if(self.IsAtEnd()):
            return '\0'#Si ya llego al final devuelve el valor predeterminado de char
        return self.input[self.current]
    def PeekNext(self):
        if(self.current + 1 >= len(self.input)):
            return '\0'
        return self.input[self.current + 1]
    def IsDigit(self,c):
        return c >= '0' and c <= '9'
    def IsAlpha(self,c):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')
    def IsFunctionOrVariable(self,c):
        if(c == 'c' or c == "s"):
            if(self.IsAlpha(self.Peek())):
                while(self.IsAlpha(self.Peek())):
                    self.Advance()
                text = self.input[self.start:self.current]
                if self.Keywords.__contains__(text):
                    token = self.Keywords[text]
                    self.tokens.append(Token(token.value,token.type,token.literal))
                else:
                    raise Exception("La funcion no se declaro correctamente")
            else:
                self.AddToken(TokenType.Variable,self.input[self.current])
        else:
            if(self.IsAlpha(self.Peek())):
                raise Exception("Las variables deben tener solo una letra")
            else:
                self.AddToken(TokenType.Variable,self.input[self.start:self.current])
    def Number(self):
        while(self.IsDigit(self.Peek())):
            self.Advance()
        if(self.Peek() == '.' and self.IsDigit(self.PeekNext())):
            self.Advance()
            while(self.IsDigit(self.Peek())):
                self.Advance()
        self.AddToken(TokenType.Numbers,float(self.input[self.start:self.current]))
    def Scan(self):
        c = self.Advance()
        if c == '(':
            self.AddToken(TokenType.LeftParenthesis,None)
        elif c == ')':
            self.AddToken(TokenType.RightParenthesis,None)
        elif c == '^':
            self.AddToken(TokenType.Pow,None)
        elif c == '+':
            self.AddToken(TokenType.Plus,None)
        elif c == '-':
            self.AddToken(TokenType.Less,None)
        elif c == '*':
            self.AddToken(TokenType.Multiply,None)
        elif c == '/':
            self.AddToken(TokenType.Divide,None)
        elif c == ' ' or c == '\r' or c == '\n':
            pass
        else:
            if self.IsDigit(c):
                self.Number()
            elif self.IsAlpha(c):
                self.IsFunctionOrVariable(c)
            else:
                raise Exception("La entrada no es correcta")
    def GetTokens(self):
        while not self.IsAtEnd():
            self.start = self.current
            self.Scan()
        self.tokens.append(Token("",TokenType.EOF,None))
        return self.tokens