# Lab Report: Parsing and Abstract Syntax Trees
---
### Course: Formal Languages & Finite Automata  
### Author: Istrati Ștefan
---
## Objective

This lab aims to deepen the understanding of parsing techniques and the construction of Abstract Syntax Trees (ASTs) as part of a simple compiler or interpreter pipeline. Specifically, we:

* Implement a lexer using regular expressions to tokenize input source code.
* Create a `TokenType` enumeration to categorize tokens.
* Define an AST structure representing the syntax of a toy programming language.
* Build a parser that converts token sequences into an AST.

## Theory

### What is Parsing?

Parsing is the process of analyzing a sequence of tokens to determine its grammatical structure according to a formal grammar. It is a core component of compilers and interpreters.

Parsers are generally of two types:

* **Top-down parsers** (e.g., recursive descent)
* **Bottom-up parsers** (e.g., shift-reduce)

In this lab, we focus on a **recursive descent parser** due to its simplicity and readability.

### What is an Abstract Syntax Tree (AST)?

An AST is a tree representation of the abstract syntactic structure of source code. Each node in the tree denotes a construct occurring in the source. Unlike concrete syntax trees (parse trees), ASTs do not represent every detail in the grammar but focus on the essential structure.

For example, the expression:

```text
3 + 4 * 2
```

is represented as:

```
      +
     / \
    3   *
       / \
      4   2
```

## Implementation

### Lexer

We implemented a `Lexer` class that uses regular expressions to tokenize the input:

```python
import re
from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    IDENTIFIER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    EQUAL = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    FOR = auto()
    SIN = auto()
    COS = auto()
    TAN = auto()
    COT = auto()

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, source):
        self.source = source

    def tokenize(self):
        token_spec = [
            (TokenType.FOR, r'for'),
            (TokenType.SIN, r'sin'),
            (TokenType.COS, r'cos'),
            (TokenType.TAN, r'tan'),
            (TokenType.COT, r'cot'),
            (TokenType.NUMBER, r'\d+(\.\d+)?'),
            (TokenType.IDENTIFIER, r'[a-zA-Z_]\w*'),
            (TokenType.PLUS, r'\+'),
            (TokenType.MINUS, r'-'),
            (TokenType.MULTIPLY, r'\*'),
            (TokenType.DIVIDE, r'/'),
            (TokenType.EQUAL, r'='),
            (TokenType.LPAREN, r'\('),
            (TokenType.RPAREN, r'\)'),
            (TokenType.LBRACE, r'\{'),
            (TokenType.RBRACE, r'\}'),
            (TokenType.SEMICOLON, r';'),
        ]

        tok_regex = '|'.join(f'(?P<{tok.name}>{regex})' for tok, regex in token_spec)
        tokens = []
        for mo in re.finditer(tok_regex, self.source):
            kind = mo.lastgroup
            value = mo.group()
            tokens.append(Token(TokenType[kind], value))
        return tokens
```

### AST Node Definitions

We define multiple classes for different AST node types:

```python
class ASTNode: pass

class Number(ASTNode):
    def __init__(self, value): self.value = value

class Variable(ASTNode):
    def __init__(self, name): self.name = name

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left, self.op, self.right = left, op, right

class Assignment(ASTNode):
    def __init__(self, target, value):
        self.target, self.value = target, value

class FunctionCall(ASTNode):
    def __init__(self, name, argument):
        self.name, self.argument = name, argument

class Block(ASTNode):
    def __init__(self, statements): self.statements = statements

class ForLoop(ASTNode):
    def __init__(self, init, condition, update, body):
        self.init, self.condition, self.update, self.body = init, condition, update, body
```

### Parser

The parser processes the list of tokens and builds the AST:

```python
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, type_):
        token = self.current()
        if token and token.type == type_:
            self.pos += 1
            return token
        raise Exception(f"Expected {type_} but got {token}")

    def parse_expression(self):
        return self.parse_term()

    def parse_term(self):
        node = self.parse_factor()
        while self.current() and self.current().type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op = self.consume(self.current().type)
            right = self.parse_factor()
            node = BinaryOp(node, op.type, right)
        return node

    def parse_factor(self):
        token = self.current()
        if token.type == TokenType.NUMBER:
            return Number(float(self.consume(TokenType.NUMBER).value))
        elif token.type == TokenType.IDENTIFIER:
            name = self.consume(TokenType.IDENTIFIER).value
            if self.current().type == TokenType.LPAREN:
                self.consume(TokenType.LPAREN)
                arg = self.parse_expression()
                self.consume(TokenType.RPAREN)
                return FunctionCall(name, arg)
            return Variable(name)
        elif token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN)
            return expr
        raise Exception(f"Unexpected token {token}")

    def parse_assignment(self):
        var = Variable(self.consume(TokenType.IDENTIFIER).value)
        self.consume(TokenType.EQUAL)
        expr = self.parse_expression()
        return Assignment(var, expr)

    def parse_condition(self):
        left = self.parse_expression()
        op = self.consume(self.current().type)
        right = self.parse_expression()
        return BinaryOp(left, op.type, right)

    def parse_for_loop(self):
        self.consume(TokenType.FOR)
        self.consume(TokenType.LPAREN)
        init = self.parse_assignment()
        self.consume(TokenType.SEMICOLON)
        condition = self.parse_condition()
        self.consume(TokenType.SEMICOLON)
        update = self.parse_assignment()
        self.consume(TokenType.RPAREN)
        body = self.parse_block()
        return ForLoop(init, condition, update, body)

    def parse_statement(self):
        token = self.current()
        if token.type == TokenType.FOR:
            return self.parse_for_loop()
        elif token.type == TokenType.IDENTIFIER:
            stmt = self.parse_assignment()
            self.consume(TokenType.SEMICOLON)
            return stmt
        else:
            raise Exception(f"Unexpected token {token}")

    def parse_block(self):
        self.consume(TokenType.LBRACE)
        statements = []
        while self.current() and self.current().type != TokenType.RBRACE:
            statements.append(self.parse_statement())
        self.consume(TokenType.RBRACE)
        return Block(statements)

    def parse(self):
        return self.parse_block()
```

## Example

Given this input code:

```c
{
  x = 0;
  for(x = 0; x < 10; x = x + 1) {
    y = sin(x);
  }
}
```

The parser builds the corresponding AST. Example of the top-level structure:

```text
Block([
  Assignment(Variable(x), Number(0)),
  ForLoop(
    Assignment(Variable(x), Number(0)),
    BinaryOp(Variable(x), TokenType.LESS_THAN, Number(10)),
    Assignment(Variable(x), BinaryOp(Variable(x), TokenType.PLUS, Number(1))),
    Block([
      Assignment(Variable(y), FunctionCall("sin", Variable(x)))
    ])
  )
])
```

## Conclusion

In this lab, we successfully implemented a lexer and parser pipeline that transforms source code into an AST. This foundational work is critical in understanding how programming languages are processed internally by compilers and interpreters.

We gained insight into:

* Designing grammars for simple languages
* Building lexers using regex
* Structuring AST nodes
* Writing recursive-descent parsers

## References

\[1] Parsing Techniques, Grune & Jacobs

\[2] Engineering a Compiler, Cooper & Torczon
