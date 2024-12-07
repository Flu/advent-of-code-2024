def load_file_into_array():
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

rules, pages = load_file_into_array()

correct_pages = []
for page in pages:
    all_correct = True
    for rule in rules:
        first_page = rule[0]
        second_page = rule[1]
        if first_page in page and second_page in page and page.index(first_page) > page.index(second_page):
            all_correct = False
    if all_correct:
        correct_pages.append(page)

import functools
print(sum([int(x[len(x)//2]) for x in correct_pages]))
