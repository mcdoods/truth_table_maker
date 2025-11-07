precedence = {
    '¬': 3,
    '.': 2,
    '+': 1
}

def main():
    expr = input("Enter expression: ").strip().upper()
    variables = get_variables(expr)
    rows = generate_combinations(expr, variables)
    rows = evaluate_expression(expr, variables, rows)
    print_table(variables, rows)

def get_variables(expr):
    variables = []
    for ch in expr:
        if 'A' <= ch <= 'Z' and ch not in variables:
            variables.append(ch)
    variables.sort()
    return variables

def generate_combinations(expr, variables):
    rows = []
    n = len(variables)
    for i in range(2 ** n):
        combo = []
        for bit in range(n-1, -1, -1):
            combo.append((i >> bit) & 1)
        rows.append(combo)
    return rows

def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        if 'A' <= ch <= 'Z':
            tokens.append(ch)
        elif ch in ('.', '+', '¬', '(', ')'):
            tokens.append(ch)
        i += 1
    return tokens

def to_postfix(tokens):
    output = []
    stack = []
    for token in tokens:
        if token.isalpha():
            output.append(token)
        elif token == '¬':
            stack.append(token)
        elif token in ('.', '+'):
            while stack and stack[-1] != '(' and precedence[stack[-1]] >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
    while stack:
        output.append(stack.pop())
    return output

def evaluate_postfix(postfix, values):
    stack = []
    for token in postfix:
        if token.isalpha():
            stack.append(values[token])
        elif token == '¬':
            a = stack.pop()
            stack.append(1 - a)
        elif token == '.':
            b = stack.pop()
            a = stack.pop()
            stack.append(a & b)
        elif token == '+':
            b = stack.pop()
            a = stack.pop()
            stack.append(a | b)
    return stack[0]

def evaluate_expression(expr, variables, rows):
    tokens = tokenize(expr)
    postfix = to_postfix(tokens)

    results = []
    for combo in rows:
        values = {variables[i]: combo[i] for i in range(len(variables))}
        result = evaluate_postfix(postfix, values)
        results.append(combo + [result])
    return results

def print_table(variables, rows):
    print(" | ".join(variables + ["F"]))
    print("-" * (4 * len(variables) + 3))
    for row in rows:
        print(" | ".join(str(x) for x in row))

main()