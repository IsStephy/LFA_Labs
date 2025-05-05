from lexer import Lexer
from parser import Parser

#code = "for (i = 0; i <= 10; i = i + 1) { sin(i); cos(i); tan(i); cot(i); if (x > y) { x = y; } }"
code = """
{
    for (i = 0; i <= 10; i = i + 1) {
        sin(i);
        cos(i);
        tan(i);
        cot(i);
        x = x + 1;
    }
}
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

print(ast)
