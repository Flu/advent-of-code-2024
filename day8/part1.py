# Advent of Code 2024 - Day 8, Part 1
# Task Description:
# Given a 2D grid with antennas, each with a different frequency, find all antinodes for pairs of 
# antennas with the same frequency. Antennas have the same frequency if they are represented
# by the same letter in the input file.
# 
# Link: https://adventofcode.com/2024/day/8
# Author: Adrian Fluturel
# Email: fluturel.adrian@gmail.com
# Date: 2024-12-08
#
# License: MIT License

def extract_from_files(filename):
    """Parses input text in the form of a 2D grid of antennas"""
    with open(filename, "r") as file:
        data = []
        while line := file.readline():
            data.append(line.strip())

    return data

def valid_coords(grid, x, y):
    """Checks if coordinates x and y are valid for a given rectangle grid."""
    if x >= 0 and x < len(grid) and y >= 0 and y < len(grid[0]):
        return True
    return False

def get_antinode(antenna1, antenna2):
    """Return a list of tuples with the coordinates of an antinode formed by antenna1 and antenna2, relative to antenna1.
        This function assumes that antenna1 and antenna2 have the same frequency."""
    x1 = antenna1[0] - (antenna2[0]-antenna1[0])
    y1 = antenna1[1] - (antenna2[1]-antenna1[1])
    return [(x1,y1)]

# Parse the contents of the input file
data = extract_from_files("input.txt")

# Group the antennas by frequency in a dictionary
frequency_location = dict()
for x, line in enumerate(data):
    for y, location in enumerate(line):
        # No antenna if character is '.'
        if location == '.':
            continue
        # Otherwise, put the antenna in a dictionary mapped to its frequency
        if location in frequency_location.keys():
            # If entry exists already, add to the list
            frequency_location[location].append((x,y))
        else:
            # If entry doesn't exist, initialize first
            frequency_location[location] = [(x,y)]

# Here we will store all antinodes
antinodes = []

# Grouped by frequency, get every combination of distinct antinodes and add them to the list 
# Get the list of antennas for a given frequency
for frequency, antenna_list in frequency_location.items():
    # For all possible combinations of two antennas in this list
    for antenna1 in antenna_list:
        for antenna2 in antenna_list:
            # Antennas have to be distinct, because a given antenna is not an antinode by itself
            if antenna1 != antenna2:
                # Add to the list the coordinates of the antinode relative to antenna1
                # This may include antinodes that are outside the map
                antinodes.extend(get_antinode(antenna1, antenna2))

# Filter antinodes outside the map
unq_antinodeds = filter(lambda x: valid_coords(data, x[0], x[1]), antinodes)

# Remove duplicates
unq_antinodeds = list(set(unq_antinodeds))

# Print all unique antinodes and how many there are
print(unq_antinodeds)
print(len(unq_antinodeds))