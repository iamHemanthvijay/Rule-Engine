-- Create Database
CREATE DATABASE IF NOT EXISTS rule_engine_db;
USE rule_engine_db;

-- Create Users Table (Stores user attributes)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    income FLOAT NOT NULL,
    department VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Rules Table (Stores the rules in JSON format)
CREATE TABLE IF NOT EXISTS rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rule_name VARCHAR(100) NOT NULL,
    rule_condition TEXT NOT NULL,  -- Store the rule condition as a JSON string
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Eligibility Results Table (Stores eligibility check results)
CREATE TABLE IF NOT EXISTS eligibility_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    rule_id INT,
    is_eligible BOOLEAN NOT NULL,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (rule_id) REFERENCES rules(id) ON DELETE CASCADE
);

-- Insert Sample Users
INSERT INTO users (name, age, income, department)
VALUES
('Alice', 30, 60000, 'IT'),
('Bob', 22, 40000, 'HR'),
('Charlie', 28, 50000, 'Finance');

-- Insert Sample Rules
INSERT INTO rules (rule_name, rule_condition)
VALUES
('Age above 25', '{"age": "> 25"}'),
('Income above 50k', '{"income": "> 50000"}'),
('Department IT', '{"department": "IT"}');

-- Insert Sample Eligibility Results
INSERT INTO eligibility_results (user_id, rule_id, is_eligible)
VALUES
(1, 1, TRUE),
(2, 2, FALSE),
(3, 3, FALSE);

-- Verify Data in Users Table
SELECT * FROM users;

-- Verify Data in Rules Table
SELECT * FROM rules;

-- Verify Data in Eligibility Results Table
SELECT * FROM eligibility_results;
