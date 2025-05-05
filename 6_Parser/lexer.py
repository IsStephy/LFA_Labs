import re
from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    IDENTIFIER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    LPAREN = auto()
    RPAREN = auto()
    EQUAL = auto()
    LESS = auto()
    LESSEQUAL = auto()
    GREATER = auto()
    GREATEREQUAL = auto()
    FOR = auto()
    WHILE = auto()
    SIN = auto()
    COS = auto()
    TAN = auto()
    COT = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()

KEYWORDS = {
    'for': TokenType.FOR,
    'while': TokenType.WHILE,
    'sin': TokenType.SIN,
    'cos': TokenType.COS,
    'tan': TokenType.TAN,
    'cot': TokenType.COT
}

TOKEN_REGEX = [
    (r'\d+\.\d+|\d+', TokenType.NUMBER),
    (r'[a-zA-Z_]\w*', 'IDENTIFIER_OR_KEYWORD'),
    (r'<=', TokenType.LESSEQUAL),
    (r'>=', TokenType.GREATEREQUAL),
    (r'<', TokenType.LESS),
    (r'>', TokenType.GREATER),
    (r'\+', TokenType.PLUS),
    (r'-', TokenType.MINUS),
    (r'\*', TokenType.MULTIPLY),
    (r'/', TokenType.DIVIDE),
    (r'\(', TokenType.LPAREN),
    (r'\)', TokenType.RPAREN),
    (r'\{', TokenType.LBRACE),
    (r'\}', TokenType.RBRACE),
    (r';', TokenType.SEMICOLON),
    (r'=', TokenType.EQUAL),
    (r'\s+', None),  # skip whitespace
]

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, text):
        self.text = text

    def tokenize(self):
        tokens = []
        pos = 0
        while pos < len(self.text):
            match = None
            for regex, type_ in TOKEN_REGEX:
                pattern = re.compile(regex)
                match = pattern.match(self.text, pos)
                if match:
                    value = match.group(0)
                    if type_:
                        if type_ == 'IDENTIFIER_OR_KEYWORD':
                            token_type = KEYWORDS.get(value, TokenType.IDENTIFIER)
                            tokens.append(Token(token_type, value))
                        else:
                            val = float(value) if type_ == TokenType.NUMBER and '.' in value else value
                            tokens.append(Token(type_, val))
                    break
            if not match:
                raise ValueError(f"Illegal character at position {pos}: {self.text[pos]}")
            else:
                pos = match.end()
        return tokens
