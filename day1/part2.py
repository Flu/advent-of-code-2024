# Advent of Code 2024 - Day 1, Part 2
# Task Description:
# Find the similarty of two lists by comparing their smallest numbers and adding all the results together
# 
# Link: https://adventofcode.com/2024/day/1
# Author: Adrian Fluturel
# Email: fluturel.adrian@gmail.com
# Date: 2024-12-04
#
# License: MIT License

def get_list_from_file(filename):
    list1 = []
    list2 = []
    with open(filename, "r") as f:
        while line := f.readline():
            numbers = line.split('   ')
            list1.append(int(numbers[0]))
            list2.append(int(numbers[1]))
    
    list1.sort()
    list2.sort()
    return list1, list2

# Get sorted lists from the input file
list1, list2 = get_list_from_file("input.txt")

# Use a dictionary to instantiate all the numbers in the first list,
# so we can check later, when going over list 2, if the numbers were present in list 1
# and count the number of appearances
mapper = dict()
for integer in list1:
    mapper[integer] = 0

for integer in list2:
    if integer in mapper.keys():
        mapper[integer] += 1

# After getting the frequency of all elements of list1 in list2, sum the key*value for all
# dictionary entries and that's the answers the Historians are looking for
sum = 0
for key, value in mapper.items():
    sum += key*value

print(sum)