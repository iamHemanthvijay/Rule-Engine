# Rule-Engine with AST

# Objective
Develop a simple 3-tier rule engine application with the following components:

1. UI: A front-end interface for user interaction.
2. API and Backend: Logic for creating and evaluating rules using AST (Abstract Syntax Tree).
3. Data Layer: A MySQL database to store rules, user data, and eligibility results.
   
The rule engine allows the dynamic creation, combination, and modification of rules based on user attributes like age, department, income, and experience. The system uses AST to represent conditional rules.

# Features

# Dynamic Rule Creation: Represent complex rules using AST.
# Rule Combination: Merge multiple rules into a single AST efficiently.
# Eligibility Evaluation: Evaluate user attributes against rules to determine eligibility.
# MySQL Integration: Store user data, rules, and results in a MySQL database.
# Validation & Error Handling: Handle invalid rule strings or missing operators gracefully.
# UI for Interaction: Simple user interface for data entry and eligibility checks.

# Technologies Used

# Frontend: HTML, CSS, JavaScript
# Backend: Python
# Database: MySQL

# Prerequisites
 Make sure you have the following installed:

 Python 3.x
 MySQL Server
 mysql-connector-python package (Install via pip install mysql-connector-python)

# Database Design
The system uses MySQL to store user data, rules, and eligibility results. Below is the schema:

# Database Schema:

-- Create Database
CREATE DATABASE IF NOT EXISTS rule_engine_db;
USE rule_engine_db;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    income FLOAT NOT NULL,
    department VARCHAR(50),
    experience INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Rules Table
CREATE TABLE IF NOT EXISTS rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rule_name VARCHAR(100) NOT NULL,
    rule_condition TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Eligibility Results Table
CREATE TABLE IF NOT EXISTS eligibility_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    rule_id INT,
    is_eligible BOOLEAN NOT NULL,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (rule_id) REFERENCES rules(id) ON DELETE CASCADE
);

-- Sample Data
INSERT INTO users (name, age, income, department, experience)
VALUES 
('Alice', 35, 70000, 'Sales', 6),
('Bob', 22, 30000, 'Marketing', 2),
('Charlie', 29, 50000, 'IT', 4);

INSERT INTO rules (rule_name, rule_condition)
VALUES 
('Rule 1', "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (income > 50000 OR experience > 5)"),
('Rule 2', "((age > 30 AND department = 'Marketing')) AND (income > 20000 OR experience > 5)");


# API Design

1. create_rule(rule_string)

 Description: Converts a rule string into an AST representation.
 Input:
 rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing'))";

 Output: Root node of the AST.

 2. combine_rules(rules)

  Description: Combines multiple ASTs into a single tree efficiently.
  
  Input: A list of rule strings.
  Output: Root node of the combined AST.

 3. evaluate_rule(json_data)

    Description: Evaluates the combined AST against user attributes.

    Input:
    json_data = { "age": 35, "department": "Sales", "income": 60000, "experience": 3 };

    output: True if the user meets the conditions, False otherwise.


# Abstract Syntax Tree (AST) Data Structure

class Node {
    constructor(type, value = null, left = null, right = null) {
        this.type = type; // "operator" or "operand"
        this.value = value; // Value for operand nodes
        this.left = left; // Left child node
        this.right = right; // Right child node
    }
}


# How to Run the Project
  
  Step 1: Install Dependencies
  
  Make sure the mysql-connector-python package is installed:
  pip install mysql-connector-python

 step 2 : Step 2: Update MySQL Credentials
 
 In the Python code, update the MySQL connection details:
 db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Adhi@luci@321",  # Replace with your MySQL password
    database="rule_engine"
)

Step 3: Run the Code

Execute the Python script using the following command:
python rule_engine.py


# Code Explanation

1. Database Connection:
   Establishes a connection to MySQL and creates the rules table if it doesn't exist.

2. Rule Creation (create_rule):
   Tokenizes the rule string and parses it into an AST.

3. Combine Rules (combine_rules):
   Takes a list of rules and combines them into a single AST.

4.Evaluate Rules (evaluate_rule):
  Evaluates the combined AST against the provided user data.

5.Test Cases (run_tests):
  Tests individual rule creation, combination, and evaluation.

# Usage Instructions

1. Create Rules: Use the backend API to define rules using create_rule.

2. Combine Rules: Combine multiple rules using combine_rules.

3. Evaluate Rules: Use the frontend UI to enter user data and check eligibility.

4. View Results: Check eligibility results stored in the MySQL database.

# Test Cases

1. Create Rule Test:

   Input: "age > 30 AND department = 'Sales'"
   Expected Output: AST representation of the rule.
   Combine Rules Test:

2. Input: Two rules as strings.
   Expected Output: Combined AST reflecting both rules.
   Evaluate Rule Test:

3. Input: JSON data like { "age": 35, "department": "Sales", "income": 60000, "experience": 3 }
   Expected Output: True or False depending on the rule conditions.

# Sample Rules and JSON Data

Example Rules:
Rule 1: ((age > 30) AND (department = 'Sales'))
Rule 2: ((age < 25) AND (department = 'Marketing'))
Rule 3: ((salary > 50000) OR (experience > 5))

test_data = [
    {"age": 35, "department": "Sales", "salary": 60000, "experience": 3},
    {"age": 22, "department": "Marketing", "salary": 40000, "experience": 1},
    {"age": 28, "department": "Sales", "salary": 70000, "experience": 6},
]

# Error Handling

The code checks for extra tokens during parsing.
Handles invalid rule formats by printing error messages.
Supports basic validations (like numeric comparisons and string matching).

# Closing the Database Connection

The MySQL connection is closed at the end of the program:

python
Copy code
cursor.close()
db.close()


# Output:

Table created successfully!
Testing individual rules:
AST for Rule 1: [['age', '>', '30'], 'AND', ['department', '=', "'Sales'"]]
AST for Rule 2: [['age', '<', '25'], 'AND', ['department', '=', "'Marketing'"]]
AST for Rule 3: [['salary', '>', '50000'], 'OR', ['experience', '>', '5']]
Combined AST: [[['age', '>', '30'], 'AND', ['department', '=', "'Sales'"]], [['age', '<', '25'], 'AND', ['department', '=', "'Marketing'"]], [['salary', '>', '50000'], 'OR', ['experience', '>', '5']]]
Testing evaluation of rules:
Evaluating data: {'age': 35, 'department': 'Sales', 'salary': 60000, 'experience': 3}
Comparing: 35 > 30
Evaluation result for ['age', '>', '30']: True
Comparing: 35 < 25
Evaluation result for ['age', '<', '25']: False
Comparing: 60000 > 50000
Evaluation result for ['salary', '>', '50000']: True
Evaluating data: {'age': 22, 'department': 'Marketing', 'salary': 40000, 'experience': 1}
Comparing: 22 > 30
Evaluation result for ['age', '>', '30']: False
Comparing: 22 < 25
Evaluation result for ['age', '<', '25']: True
Comparing: 40000 > 50000
Evaluation result for ['salary', '>', '50000']: False
Evaluating data: {'age': 28, 'department': 'Sales', 'salary': 70000, 'experience': 6}
Comparing: 28 > 30
Evaluation result for ['age', '>', '30']: False
Comparing: 28 < 25
Evaluation result for ['age', '<', '25']: False
Comparing: 70000 > 50000
Evaluation result for ['salary', '>', '50000']: True




  






























