from lexer import TokenType, Lexer, Token

class ASTNode:
    pass

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name})"

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.left}, '{self.op.name}', {self.right})"

class Assignment(ASTNode):
    def __init__(self, target, value):
        self.target = target
        self.value = value

    def __repr__(self):
        return f"Assignment({self.target}, {self.value})"

class FunctionCall(ASTNode):
    def __init__(self, name, argument):
        self.name = name
        self.argument = argument

    def __repr__(self):
        return f"\nFunctionCall('{self.name}', {self.argument})"

class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"\nBlock({self.statements})"

class ForLoop(ASTNode):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def __repr__(self):
        return (f"\nForLoop(init={self.init}, condition={self.condition}, "
                f"update={self.update}, body={self.body})")

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

    def parse_number(self):
        token = self.consume(TokenType.NUMBER)
        return Number(token.value)

    def parse_variable_or_function(self):
        name = self.consume(TokenType.IDENTIFIER).value
        if self.current() and self.current().type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            arg = self.parse_expression()
            self.consume(TokenType.RPAREN)
            return FunctionCall(name, arg)
        return Variable(name)

    def parse_factor(self):
        token = self.current()
        if token.type == TokenType.NUMBER:
            return self.parse_number()
        elif token.type == TokenType.IDENTIFIER:
            return self.parse_variable_or_function()
        elif token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN)
            return expr
        raise Exception(f"Unexpected token {token}")

    def parse_term(self):
        node = self.parse_factor()
        while self.current() and self.current().type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op = self.consume(self.current().type)
            right = self.parse_factor()
            node = BinaryOp(node, op.type, right)
        return node

    def parse_expression(self):
        node = self.parse_term()
        while self.current() and self.current().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.consume(self.current().type)
            right = self.parse_term()
            node = BinaryOp(node, op.type, right)
        return node

    def parse_assignment(self):
        var_name = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.EQUAL)
        expr = self.parse_expression()
        return Assignment(Variable(var_name), expr)

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
        elif token.type in (TokenType.SIN, TokenType.COS, TokenType.TAN, TokenType.COT):
            func_token = self.consume(token.type)
            self.consume(TokenType.LPAREN)
            arg = self.parse_expression()
            self.consume(TokenType.RPAREN)
            self.consume(TokenType.SEMICOLON)
            return FunctionCall(func_token.type.name.lower(), arg)
        else:
            raise Exception(f"Unknown statement starting with {token}")

    def parse_block(self):
        self.consume(TokenType.LBRACE)
        statements = []
        while self.current() and self.current().type != TokenType.RBRACE:
            statements.append(self.parse_statement())
        self.consume(TokenType.RBRACE)
        return Block(statements)

    def parse(self):
        return self.parse_block()
