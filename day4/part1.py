# Advent of Code 2024 - Day 4, Part 1
# Task Description:
# In a grid of letters, find all occurences of the word 'XMAS', in vertical, horizontal, diagonal position,
# forwards or reversed.
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
    
    def checkHorizontallyForwards(self, row, column, word = "XMAS"):
        return self.text[row][column:min(self.width(), column+len(word))] == word
    
    def checkHorizontallyBackwards(self, row, column, word = "XMAS"):
        return self.text[row][max(0, column-len(word)+1): column+1] == word[::-1]

    def checkWordVerticallyForwards(self, row, column, word = "XMAS"):
        found_rows = self.text[row:min(self.height(), row+len(word))]
        result = ""
        for row in found_rows:
            result += row[column]
        return result == word
    
    def checkWordVerticallyBackwards(self, row, column, word = "XMAS"):
        found_rows = self.text[max(0, row-len(word)+1): row+1]
        result = ""
        for row in found_rows:
            result += row[column]
        return result == word[::-1]

    def checkWordDiagonally(self, row, col, word = "XMAS"):
        word_len = len(word)
        all_occurences = 0
        # bottom-right diagonal
        if row + word_len <= self.height() and col + word_len <= self.width():
            if all(self.text[row + i][col + i] == word[i] for i in range(word_len)):
                all_occurences += 1

        # bottom-left diagonal
        if row + word_len <= self.height() and col - word_len >= -1:
            if all(self.text[row + i][col - i] == word[i] for i in range(word_len)):
                all_occurences += 1

        # top-right diagonal
        if row - word_len >= -1 and col + word_len <= self.width():
            if all(self.text[row - i][col + i] == word[i] for i in range(word_len)):
                all_occurences += 1

        # top-left diagonal
        if row - word_len >= -1 and col - word_len >= -1:
            if all(self.text[row - i][col - i] == word[i] for i in range(word_len)):
                all_occurences += 1

        return all_occurences

grid = Grid(load_file_into_array())

occurences = 0
word_to_look_for = "XMAS"

for row in range(grid.height()):
    for col in range(grid.width()):
        if grid.get(row, col) != word_to_look_for[0]:
            continue
        if grid.checkHorizontallyForwards(row, col):
            occurences += 1
        if grid.checkHorizontallyBackwards(row, col):
            occurences += 1
        if grid.checkWordVerticallyForwards(row, col):
            occurences += 1
        if grid.checkWordVerticallyBackwards(row, col):
            occurences += 1
        if (diagonal_occurences := grid.checkWordDiagonally(row, col)) != 0:
            occurences += diagonal_occurences

print(occurences)