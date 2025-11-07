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

def evaluate_expression(expr, variables, rows):
    safe_expr = expr.replace(".", " and ").replace("+", " or ").replace("¬", " not ")
    
    for combo in rows:
        env = {variables[i]: combo[i] for i in range(len(variables))}
        eval_expr = safe_expr
        for var, val in env.items():
            eval_expr = eval_expr.replace(var, str(bool(val)))
        result = eval(eval_expr)
        combo.append(int(result))
        
    return rows

def print_table(variables, rows):
    print(" | ".join(variables + ["F"]))
    print("-" * (4 * len(variables) + 5))
    
    for row in rows:
        print(" | ".join(str(x) for x in row))

def main():
    print("¬ = NOT, . = AND, + = OR")
    expr = input("Enter expression: ").strip().upper()
    
    variables = get_variables(expr)
    rows = evaluate_expression(expr, variables, generate_combinations(expr, variables))
    print_table(variables, rows)
    
main()