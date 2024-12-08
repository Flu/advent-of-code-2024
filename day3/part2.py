# Advent of Code 2024 - Day 3, Part 2
# Task Description:
# In a corrupted "binary file", find all the correctly written multiplication commands of form "mul(a,b)" where
# a and b are positive integers. Do the calculation and accumulate all results in a sum. When a do() command is found,
# enable multiplications, when a don't() command is found, ignore all multiplications until the next do().
# 
# Link: https://adventofcode.com/2024/day/3
# Author: Adrian Fluturel
# Email: fluturel.adrian@gmail.com
# Date: 2024-12-04
#
# License: MIT License

file_string = ""
with open("input.txt", "r") as f:
    file_string = f.readlines()

# Join all the lines into one big string since we don't care about different lines
file_string = "".join(file_string)

# Use regex to extract the numbers with capture groups
# This is much less work than it would have been just parsing it normally
# Note: Now we will have two more capture groups that we can use to identify in which case we are
import re
p = re.compile(r"mul\(([\d]+),([\d]+)\)|(do\(\))|(don't\(\))")
results = p.findall(file_string)


final_sum = 0

# By default, multiplication is enabled
enable_mul = True

# For all matches, we can extract the numbers from their respective capture groups, parse them as ints
# and multiply them and finally add them to the final sum, if multiplication is enabled
for result in results:
    if result[2] == "do()":
        enable_mul = True
    elif result[3] == "don't()":
        enable_mul = False
    elif enable_mul == True:
        number1 = int(result[0])
        number2 = int(result[1])
        final_sum += number1 * number2

print(final_sum)
