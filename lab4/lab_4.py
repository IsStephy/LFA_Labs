import random
import re

MAX_REPEAT = 5
trace_log = []

def generate_from_regex(pattern):
    trace_log.append(f"Processing pattern: {pattern}")
    tokens = tokenize(pattern)
    ast = parse(tokens)
    return evaluate(ast)

def tokenize(pattern):
    tokens = []
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if c in '()*+|':
            tokens.append(c)
            i += 1
        elif c == '{':
            j = i + 1
            while j < len(pattern) and pattern[j] != '}':
                j += 1
            tokens.append(pattern[i:j+1])  # Include closing }
            i = j + 1
        else:
            tokens.append(c)
            i += 1
    return tokens

def parse(tokens):
    output = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '(':
            # parse group
            sub_tokens = []
            depth = 1
            i += 1
            while i < len(tokens):
                if tokens[i] == '(':
                    depth += 1
                elif tokens[i] == ')':
                    depth -= 1
                    if depth == 0:
                        break
                sub_tokens.append(tokens[i])
                i += 1
            sub_ast = parse(sub_tokens)
            output.append(sub_ast)
        elif token == '|':
            left = output
            right = parse(tokens[i + 1:])
            return [('OR', left, right)]
        elif token == '*':
            output[-1] = ('STAR', output[-1])
        elif token == '+':
            output[-1] = ('PLUS', output[-1])
        elif re.fullmatch(r'\{[0-9]+\}', token):
            count = int(token.strip('{}'))
            output[-1] = ('REPEAT', output[-1], count)
        else:
            output.append(('LIT', token))
        i += 1
    return output

def evaluate(ast):
    result = ''
    for node in ast:
        result += eval_node(node)
    return result

def eval_node(node):
    kind = node[0]
    if kind == 'LIT':
        trace_log.append(f"Literal: {node[1]}")
        return node[1]
    elif kind == 'REPEAT':
        sub, count = node[1], node[2]
        trace_log.append(f"Repeat exactly {count} times")
        return ''.join(eval_node(sub) for _ in range(count))
    elif kind == 'STAR':
        count = random.randint(0, MAX_REPEAT)
        trace_log.append(f"Repeat 0 to {MAX_REPEAT} times (actual: {count})")
        return ''.join(eval_node(node[1]) for _ in range(count))
    elif kind == 'PLUS':
        count = random.randint(1, MAX_REPEAT)
        trace_log.append(f"Repeat 1 to {MAX_REPEAT} times (actual: {count})")
        return ''.join(eval_node(node[1]) for _ in range(count))
    elif kind == 'OR':
        left, right = node[1], node[2]
        chosen = random.choice([left, right])
        trace_log.append(f"Choosing one option from OR")
        return ''.join(eval_node(n) for n in chosen)
    else:
        return ''.join(eval_node(n) for n in node)
regexes = [
    "(S|T)(u|v)w*y+24",
    "L(l|m|n)o{3}p*q(2|3)",
    "R*s(t|u|v)w(x|y|z){2}"
]

for i, pattern in enumerate(regexes, 1):
    trace_log = []
    generated = generate_from_regex(pattern)
    print(f"\nGenerated string for regex {i}: {pattern} → {generated}")
    print("Trace:")
    for step in trace_log:
        print("  -", step)