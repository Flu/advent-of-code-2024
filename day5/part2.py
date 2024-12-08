# Advent of Code 2024 - Day 5, Part 2
# Task Description:
# Given a list of rules of the form a|b, where a and positive integers, then some lists of integers, find all lists that
# respect the rule "a should be before b in the list".
# Get all the lists that don't obey the rules and fix them, then take the middle number in the list and add it to the accumulator.
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

def check_page_is_correct(page, rules):
    """Check if a page is correct according to the rules"""
    all_correct = True
    for rule in rules:
        first_page = rule[0]
        second_page = rule[1]
        if first_page in page and second_page in page and page.index(first_page) > page.index(second_page):
            all_correct = False
    return all_correct

rules, pages = load_file_into_array()

# Get the wrong pages
wrong_pages = []
for page in pages:
    all_correct = check_page_is_correct(page, rules)
    if not all_correct:
        wrong_pages.append(page)

# Fix the pages by finding what rule they broke and swapping the pages that are in the wrong order
for page in wrong_pages:
    # While the page is still wrong
    while not check_page_is_correct(page, rules):
        all_correct = True
        # Go through all the rules
        for rule in rules:
            first_page = rule[0]
            second_page = rule[1]
            if first_page in page and second_page in page and page.index(first_page) > page.index(second_page):
                # Swap pages and check for correctness again
                page[page.index(first_page)], page[page.index(second_page)] = page[page.index(second_page)], page[page.index(first_page)]
                all_correct = False

# Print the middle number in all lists that have been fixed
print(sum([int(x[len(x)//2]) for x in wrong_pages]))
