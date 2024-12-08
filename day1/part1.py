# Advent of Code 2024 - Day 1, Part 1
# Task Description:
# Find the similarty of two lists by comparing their smallest numbers and adding all the results together
# 
# Link: https://adventofcode.com/2024/day/1
# Author: Adrian Fluturel
# Email: fluturel.adrian@gmail.com
# Date: 2024-12-04
#
# License: MIT License

def get_lists_from_file(filename):
    list1 = []
    list2 = []
    with open(filename, "r") as f:
        while line := f.readline():
            numbers = line.split('   ')
            list1.append(int(numbers[0]))
            list2.append(int(numbers[1]))
    return list1, list2

# Extract lists from the input file
list1, list2 = get_lists_from_file("input.txt")

# Sort all the lists so we can compare the smallest elements
list1.sort()
list2.sort()

# Get the absolute value of the difference of all elements in the sorted list
result = sum([abs(list1[i]-list2[i]) for i in range(len(list1))])
print("The difference between the lists:", result)