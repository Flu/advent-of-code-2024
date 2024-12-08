# Advent of Code 2024 - Day 5, Part 1
# Task Description:
# Given a list of rules of the form a|b, where a and positive integers, then some lists of integers, find all lists that
# respect the rule "a should be before b in the list". If a list obeys all rules, take the middle page and add it to the
# accumulator.
# 
# Link: https://adventofcode.com/2024/day/5
# Author: Adrian Fluturel
# Email: fluturel.adrian@gmail.com
# Date: 2024-12-05
#
# License: MIT License

def load_file_into_array():
    """Load rules and pages from the input file into separate lists"""
    rules = []
    pages = []
    with open("input.txt", "r") as f:
        while line := f.readline():
            if line == '\n':
                break
            rules.append(line.strip().split("|"))

        while line := f.readline():
            pages.append(line.strip().split(","))
    return rules, pages

# Get all pages and rules from input
rules, pages = load_file_into_array()

# List to hold all correct pages
# Could have also summed the middle numbers of every correct list here directly,
# but during the exercise, I needed to see the lists that my program deemed correct
# for debugging purposes
correct_pages = []
for page in pages:
    # Assume all rules are obeyed by the list
    all_correct = True
    for rule in rules:
        first_page = rule[0]
        second_page = rule[1]
        # If index of page a is larger than the index of page b, they are in the wrong order
        if first_page in page and second_page in page and page.index(first_page) > page.index(second_page):
            all_correct = False
    # If all rules are obeyed, add the page to the list
    if all_correct:
        correct_pages.append(page)

# Print the middle number in all lists that have been fixed
print(sum([int(x[len(x)//2]) for x in correct_pages]))
