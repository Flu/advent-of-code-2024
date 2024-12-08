# Advent of Code 2024 - Day 7, Part 2
# Task Description:
# Get a list of expressions of the form result -> a b c d... 
# Given the operations +, * and concatenation ('|') find the combination of operands and operations such that it results
# in result. There is no operator precedence here to take into account, all expressions are executed left-to-right.
# 
# Link: https://adventofcode.com/2024/day/7
# Author: Adrian Fluturel
# Email: fluturel.adrian@gmail.com
# Date: 2024-12-07
#
# License: MIT License

from itertools import product

def extract_numbers(file_name):
    results = []
    with open(file_name, 'r') as file:
        for line in file:
            # Split line into parts, ignoring the colon
            parts = line.replace(":", "").split()
            # Convert to integers and append to results
            results.append(list(map(int, parts)))
    return results

def evaluate_expression(numbers, operators):
    result = numbers[0]
    for i, operator in enumerate(operators):
        if operator == '+':
            result += numbers[i + 1]
        elif operator == '*':
            result *= numbers[i + 1]
        elif operator == "|":
            result = int(str(result) + str(numbers[i+1]))
    return result

def find_operations(lists):
    results = []
    for lst in lists:
        target = lst[0]
        numbers = lst[1:]

        for ops in product("+*|", repeat=len(numbers) - 1):
            if evaluate_expression(numbers, ops) == target:
                expression = f"{numbers[0]}"
                for num, op in zip(numbers[1:], ops):
                    expression += f" {op} {num}"
                results.append((lst, expression))
                break
    return results

file_name = "input.txt"
numbers = extract_numbers(file_name)

result = find_operations(numbers)
sum = 0
for list, expression in result:
    print(f"List: {list} -> Expression: {expression}")
    sum += list[0]

print(sum)