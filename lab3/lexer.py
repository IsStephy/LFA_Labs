import math

TOKEN_TYPES = {
    'NUMBER': 'NUMBER',
    'IDENTIFIER': 'IDENTIFIER',
    'PLUS': '+',
    'MINUS': '-',
    'MULTIPLY': '*',
    'DIVIDE': '/',
    'LPAREN': '(',
    'RPAREN': ')',
    'EQUAL': '=',
    'LESS': '<',
    'LESSEQUAL': '<=',
    'GREATER': '>',
    'GREATEREQUAL': '>=',
    'FOR': 'FOR',
    'WHILE': 'WHILE',
    'SIN': 'SIN',
    'COS': 'COS',
    'TAN': 'TAN',
    'COT': 'COT',
    'LBRACE': '{',
    'RBRACE': '}',
    'SEMICOLON': ';'
}

KEYWORDS = {
    "for": "FOR",
    "while": "WHILE",
    "sin": "SIN",
    "cos": "COS",
    "tan": "TAN",
    "cot": "COT"
}

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position] if self.text else None

    def advance(self):
        """Move to the next character."""
        self.position += 1
        self.current_char = self.text[self.position] if self.position < len(self.text) else None

    def peek(self):
        """Look at the next character without advancing."""
        next_pos = self.position + 1
        return self.text[next_pos] if next_pos < len(self.text) else None

    def skip_whitespace(self):
        """Skip spaces and tabs."""
        while self.current_char is not None and self.current_char in ' \t':
            self.advance()

    def get_number(self):
        """Extracts a number (integer or float)."""
        num_str = ''
        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        
        if self.current_char == '.': 
            num_str += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                num_str += self.current_char
                self.advance()
        
        return Token(TOKEN_TYPES['NUMBER'], float(num_str) if '.' in num_str else int(num_str))

    def get_identifier(self):
        """Extracts an identifier (variable name or keyword)."""
        ident_str = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            ident_str += self.current_char
            self.advance()

        token_type = KEYWORDS.get(ident_str, 'IDENTIFIER')
        return Token(token_type, ident_str)

    def get_next_token(self):
        """Extracts the next token from the input text."""
        while self.current_char is not None:
            if self.current_char in ' \t':
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return self.get_number()
            if self.current_char.isalpha():
                return self.get_identifier()
            if self.current_char == '+':
                self.advance()
                return Token('PLUS', '+')
            if self.current_char == '-':
                self.advance()
                return Token('MINUS', '-')
            if self.current_char == '*':
                self.advance()
                return Token('MULTIPLY', '*')
            if self.current_char == '/':
                self.advance()
                return Token('DIVIDE', '/')
            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')
            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')
            if self.current_char == '=':
                self.advance()
                return Token('EQUAL', '=')
            if self.current_char == '{':
                self.advance()
                return Token('LBRACE', '{')
            if self.current_char == '}':
                self.advance()
                return Token('RBRACE', '}')
            if self.current_char == ';':
                self.advance()
                return Token('SEMICOLON', ';')
            if self.current_char == '<':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token('LESSEQUAL', '<=')
                self.advance()
                return Token('LESS', '<')
            if self.current_char == '>':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token('GREATEREQUAL', '>=')
                self.advance()
                return Token('GREATER', '>')

            raise ValueError(f"Unrecognized character: {self.current_char}")

        return None

    def tokenize(self):
        """Tokenizes the entire input string."""
        tokens = []
        while (token := self.get_next_token()) is not None:
            tokens.append(token)
        return tokens

code = "for (i = 0; i <= 10; i = i + 1) { sin(i); cos(i); tan(i); cot(i); if (x > y) { x = y; } }"
lexer = Lexer(code)
tokens = lexer.tokenize()

for token in tokens:
    print(token)
