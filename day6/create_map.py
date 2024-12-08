# Create a random map to test part1.py and part2.py. Not part of the official challenge, just fun
# 
# Link: https://adventofcode.com/2024/day/6
# Author: Adrian Fluturel
# Email: fluturel.adrian@gmail.com
# Date: 2024-12-06
#
# License: MIT License


result = ""
width = 500
height = 500

import random as r

for i in range(height):
    row = r.choices([".", "#"], [0.99, 0.01], k=width)
    result += "".join(row) + "\n"

with open("ultra_test.txt", "w") as f:
    f.write(result)