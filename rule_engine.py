import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Adhi@luci@321",
    database="rule_engine"
)

cursor = db.cursor()

# Create table
cursor.execute("CREATE TABLE IF NOT EXISTS rules (id INT AUTO_INCREMENT PRIMARY KEY, rule_text VARCHAR(255))")
print("Table created successfully!")

# Function to insert rules
def insert_rule(rule):
    cursor.execute("INSERT INTO rules (rule_text) VALUES (%s)", (rule,))
    db.commit()
    print("Rule inserted successfully!")

# Function to create AST from a rule
def create_rule(rule):
    tokens = tokenize(rule)
    root, remaining_tokens = parse_tokens(tokens)
    if remaining_tokens:
        print(f"Error creating rule from '{rule}': Extra tokens remaining after parsing.")
        return None
    return root

# Tokenize function
def tokenize(rule):
    return rule.replace('(', ' ( ').replace(')', ' ) ').split()

# Parsing tokens function
def parse_tokens(tokens):
    if not tokens:
        return None, tokens

    token = tokens.pop(0)
    if token == '(':
        sub_expr = []
        while tokens[0] != ')':
            node, tokens = parse_tokens(tokens)
            sub_expr.append(node)
        tokens.pop(0)  # Remove the ')'
        return sub_expr, tokens
    elif token == ')':
        raise ValueError("Unexpected token: )")
    else:
        return token, tokens

# Function to combine rules into an AST
def combine_rules(rules):
    ast_nodes = []
    for rule in rules:
        ast_node = create_rule(rule)
        if ast_node is None:
            print(f"Error creating rule from '{rule}'")
        else:
            ast_nodes.append(ast_node)
    if not ast_nodes:
        print("No valid AST created from rules.")
        return None
    return ast_nodes

# Function to evaluate rule
def evaluate_rule(ast, data):
    if isinstance(ast, list):
        if len(ast) == 3:  # Basic condition
            left = ast[0]
            operator = ast[1]
            right = ast[2].strip("'")  # Strip quotes for string comparisons

            left_value = data.get(left)

            # Handle numeric comparisons
            if isinstance(left_value, str) and left_value.isdigit():
                left_value = int(left_value)
            if right.isdigit():  # Ensure right side is treated as an int if it's numeric
                right = int(right)

            # Debug print statements
            print(f"Comparing: {left_value} {operator} {right}")

            # Perform comparison
            if operator == '>':
                return left_value > right
            elif operator == '<':
                return left_value < right
            elif operator == '=':
                return str(left_value) == str(right)  # Compare as strings for department

        elif len(ast) == 5:  # AND/OR condition
            left_result = evaluate_rule(ast[0], data)
            operator = ast[1]
            right_result = evaluate_rule(ast[2], data)

            # Combine results based on the operator
            if operator == 'AND':
                return left_result and right_result
            elif operator == 'OR':
                return left_result or right_result

    return False  # Default return value for invalid input

# Test cases
def run_tests():
    # Test 1: Create individual rules and verify AST representation
    rule1 = "((age > 30) AND (department = 'Sales'))"
    rule2 = "((age < 25) AND (department = 'Marketing'))"
    rule3 = "((salary > 50000) OR (experience > 5))"

    print("Testing individual rules:")
    ast1 = create_rule(rule1)
    ast2 = create_rule(rule2)
    ast3 = create_rule(rule3)
    print(f"AST for Rule 1: {ast1}")
    print(f"AST for Rule 2: {ast2}")
    print(f"AST for Rule 3: {ast3}")

    # Test 2: Combine example rules
    combined_rules = [rule1, rule2, rule3]
    combined_ast = combine_rules(combined_rules)
    print(f"Combined AST: {combined_ast}")

    # Test 3: Evaluate rule with sample JSON data
    test_data = [
        {"age": 35, "department": "Sales", "salary": 60000, "experience": 3},
        {"age": 22, "department": "Marketing", "salary": 40000, "experience": 1},
        {"age": 28, "department": "Sales", "salary": 70000, "experience": 6},
    ]
    print("Testing evaluation of rules:")
    for data in test_data:
        print(f"Evaluating data: {data}")
        for ast in combined_ast:
            # Evaluate each individual AST
            result = evaluate_rule(ast[0], data)  
            print(f"Evaluation result for {ast[0]}: {result}")

# Execute test cases
run_tests()

# Close database connection
cursor.close()
db.close()
