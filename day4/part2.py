# Advent of Code 2024 - Day 4, Part 2
# Task Description:
# In a grid of letters, find all occurences of 'MAS' or 'SAM' in a cross pattern:
# .M.S.
# ..A..
# .M.S.
# 
# Link: https://adventofcode.com/2024/day/4
# Author: Adrian Fluturel
# Email: fluturel.adrian@gmail.com
# Date: 2024-12-04
#
# License: MIT License

def load_file_into_array():
    text = []
    with open("input.txt", "r") as f:
        while line := f.readline():
            text.append(line.strip())

    return text


class Grid:
    def __init__(self, text_corpus):
        self.text = text_corpus

    def get(self, row, column):
        return self.text[row][column]
    
    def width(self):
        return len(self.text[0])
    
    def height(self):
        return len(self.text)
    

grid = Grid(load_file_into_array())
occurences = 0

for row in range(1, grid.height() - 1):
    for col in range(1, grid.width() - 1):
        if grid.get(row, col) != 'A':
            continue
        
        negative_slope_diagonal = False
        # If this is true, we have a MAS on the negative slope diagonal
        if (grid.get(row-1, col-1) == 'M' and grid.get(row+1, col+1) == 'S') \
            or (grid.get(row-1, col-1) == 'S' and grid.get(row+1, col+1) == 'M'):
            negative_slope_diagonal = True

        positive_slope_diagonal = False
        # If this is true, we have a MAS on the negative slope diagonal
        if (grid.get(row-1, col+1) == 'M' and grid.get(row+1, col-1) == 'S') \
            or (grid.get(row-1, col+1) == 'S' and grid.get(row+1, col-1) == 'M'):
            positive_slope_diagonal = True

        if negative_slope_diagonal and positive_slope_diagonal:
            occurences += 1

print(occurences)