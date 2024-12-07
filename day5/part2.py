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

def check_page_is_correct(page, rules):
    all_correct = True
    for rule in rules:
        first_page = rule[0]
        second_page = rule[1]
        if first_page in page and second_page in page and page.index(first_page) > page.index(second_page):
            all_correct = False
    return all_correct

rules, pages = load_file_into_array()

# geet the wrong pages
wrong_pages = []
for page in pages:
    all_correct = check_page_is_correct(page, rules)
    if not all_correct:
        wrong_pages.append(page)

# fix the pages

for page in wrong_pages:
    while not check_page_is_correct(page, rules):
        all_correct = True
        for rule in rules:
            first_page = rule[0]
            second_page = rule[1]
            if first_page in page and second_page in page and page.index(first_page) > page.index(second_page):
                page[page.index(first_page)], page[page.index(second_page)] = page[page.index(second_page)], page[page.index(first_page)]
                all_correct = False


import functools
print(sum([int(x[len(x)//2]) for x in wrong_pages]))
