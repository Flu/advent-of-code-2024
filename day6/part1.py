# Advent of Code 2024 - Day 6, Part 1
# Task Description:
# Given a grid of cells, a cell can be a player, an obstace or empty space. 
# The player has a starting orientation of UP. When simulating the player, the player will start going
# up until it hits an obstacle, at which point, it will rotate 90° to the right and keeps going. The 
# simulation is considered over when the player exits the bound of the map. The map is always a rectangle.
# The goal is to return the number of cells visited by the player.
# 
# Link: https://adventofcode.com/2024/day/6
# Author: Adrian Fluturel
# Email: fluturel.adrian@gmail.com
# Date: 2024-12-06
#
# License: MIT License

from typing import List, Self, Tuple, Optional
from enum import Enum

class Cell:
    """Cell class to hold the state of a cell, visited or an obstacle"""
    
    def __init__(self: Self, isVisited: bool, isObstacle: bool) -> None:
        self.visited = isVisited
        self.obstacle = isObstacle


class Orientation(Enum):
    """Orientation class for the player"""
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def rotate(self) -> Self:
        """Take the given orienation and rotate 90° to the right"""
        if self == Orientation.UP:
            return Orientation.RIGHT
        elif self == Orientation.DOWN:
            return Orientation.LEFT
        elif self == Orientation.LEFT:
            return Orientation.UP
        else:
            return Orientation.DOWN

class Map:
    """Class for holding player information and the map itself"""

    def __init__(self: Self, lines: List[List[str]]) -> None:
        """Takes a list of lists of strings with the raw characters, as they are in the input file. Takes every position and
        categorizes it based on the state of the cell. It also finds the player and initializes player-related fields like 
        the position, orientation."""
        self.grid = []
        self.player_posx = 0
        self.player_posy = 0
        self.orientation = Orientation.UP

        for line_index, line in enumerate(lines):
            row = []
            for char_index, char in enumerate(line):
                if char == '.':
                    row.append(Cell(False, False))
                if char == '#':
                    row.append(Cell(False, True))
                if char == '>' or char == '^' or char == '<':
                    row.append(Cell(True, False))
                    self.player_posx = line_index
                    self.player_posy = char_index
            self.grid.append(row)

        self.__rows = len(lines)
        self.__columns = len(lines[0])

    def how_many_visited(self: Self) -> int:
        """Traverses the whole map and counts all cells that were visited, returns the count"""
        count = 0
        for line in self.grid:
            for cell in line:
                count += 1 if cell.visited == True else 0
        return count

    def get(self: Self, row: int, column: int) -> Cell:
        """Returns the cell at the given row and column indices"""
        return self.grid[row][column]
    
    def rows(self: Self) -> int:
        """Returns the number of rows in the map"""
        return self.__rows
    
    def columns(self: Self) -> int:
        """Returns the number of columns in the map"""
        return self.__columns
    
    def until_next_obstacle(self: Self) -> Optional[Tuple[int, int]]:
        """Run the simulation until the player gets at the next obstacle.
        Returns None if the simulation is done (we've exited the map).
        Returns the last valid coordinates of the player after hitting an obstacle. It also rotates the player."""

        # Calculate the dx and dy based on the orientation of the player
        x_offset = 0
        y_offset = 0
        if self.orientation == Orientation.UP:
            x_offset = -1
        if self.orientation == Orientation.DOWN:
            x_offset = +1
        if self.orientation == Orientation.LEFT:
            y_offset = -1
        if self.orientation == Orientation.RIGHT:
            y_offset = +1

        while True:
            # Set current cell as visited
            self.get(self.player_posx, self.player_posy).visited = True

            # If the coordinates of the next cell to be visited are not valid anymore, it means
            # we've exited the map and the simulation is done, return None to signify that
            if not self.valid_coords(self.player_posx + x_offset, self.player_posy + y_offset):
                return None
            
            # If we've hit an obstacle, don't advance any further, change orientation and return current coordinates
            if self.get(self.player_posx + x_offset, self.player_posy + y_offset).obstacle == True:
                self.orientation = self.orientation.rotate()
                return self.player_posx, self.player_posy
            
            # Otherwise, it means we still have some way to go, so increment x and y position with the offsets
            self.player_posx += x_offset
            self.player_posy += y_offset
    
    def step(self: Self) -> Optional[List[int]]:
        """Run the simulation for one step. When it hits an obstacle, it first rotates the player then returns.
        Returns None if the simulation is done (we've exited the map).
        Returns the last valid coordinates of the player."""
        new_coords = [self.player_posx,self.player_posy]
        if self.orientation == Orientation.UP:
            new_coords[0] -= 1
        if self.orientation == Orientation.DOWN:
            new_coords[0] += 1
        if self.orientation == Orientation.LEFT:
            new_coords[1] -= 1
        if self.orientation == Orientation.RIGHT:
            new_coords[1] += 1

        # If the new coordinates are not valid, it means we've exited the map
        if not self.valid_coords(new_coords[0], new_coords[1]):
            return None
        
        # If the new coordinates are an obstacle, rotate 90 degrees and don't change current coords
        if self.grid[new_coords[0]][new_coords[1]].obstacle == True:
            print("Obstacle at", new_coords, ", rotating to ", self.orientation.rotate())
            self.orientation = self.orientation.rotate()
            return [self.player_posx, self.player_posy]
        
        # If the coordinates are valid and there is no obstacle, set player coordinates to new_coords
        # and mark the node as visited
        self.player_posx = new_coords[0]
        self.player_posy = new_coords[1]
        self.get(self.player_posx, self.player_posy).visited = True
        return new_coords
        
    def valid_coords(self: Self, x: int, y: int) -> bool:
        """Checks if x and y are valid coordinates in the current map"""
        if x < 0 or x >= self.columns():
            return False
        if y < 0 or y >= self.rows():
            return False
        return True
    
def load_file_into_array(filename: str) -> List[List[str]]:
    """Writes the grid into a list of lists of strings that will later be parsed by the Map object"""
    text = []
    with open(filename, "r") as f:
        while line := f.readline():
            text.append(line.strip())

    return text

def run_simulation(grid: Map) -> int:
    """Given a map, run the simulation until the simulation ends.
    If it does end, return the number of visited cells."""
    while result := grid.until_next_obstacle():
        if result is None:
            break
    return grid.how_many_visited()


raw_data = load_file_into_array("ultra_test.txt")
grid = Map(raw_data)

import time
 
print("Initial X: ", grid.player_posx)
print("Initial Y: ", grid.player_posy)

start_time = time.process_time()
run_simulation(grid)
end_time = time.process_time()
print(grid.how_many_visited())
print("Total time:", end_time-start_time)