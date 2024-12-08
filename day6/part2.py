# Advent of Code 2024 - Day 6, Part 2
# Task Description:
# Given a grid of cells, a cell can be a player, an obstace or empty space. 
# The player has a starting orientation of UP. When simulating the player, the player will start going
# up until it hits an obstacle, at which point, it will rotate 90° to the right and keeps going. The 
# simulation is considered over when the player exits the bound of the map. The map is always a rectangle.
# The goal is to find all maps, that when added an obstacle to the initial one, make the player enter an infinite loop.
# 
# Link: https://adventofcode.com/2024/day/6
# Author: Adrian Fluturel
# Email: fluturel.adrian@gmail.com
# Date: 2024-12-06
#
# License: MIT License

from typing import List, Self, Optional, Tuple
from enum import Enum
import time

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

    def rotate(self: Self) -> Self:
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

    def __init__(self: Self, lines: List[List[str]] = None) -> None:
        """Takes an optional list of lists of strings with the raw characters, as they are in the input file. Takes every position and
        categorizes it based on the state of the cell. It also finds the player and initializes player-related fields like 
        the position, orientation."""
        self.grid = []
        self.player_posx = 0
        self.player_posy = 0
        self.orientation = Orientation.UP
        self.moves = 0

        self.__rows = 0
        self.__columns = 0

        if lines is None:
            return
        
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

        self.__rows = len(self.grid)
        self.__columns = len(self.grid[0])

    def how_many_visited(self: Self) -> int:
        """Traverses the whole map and counts all cells that were visited, returns the count"""
        count = 0
        for line in self.grid:
            for cell in line:
                count += 1 if cell.visited == True else 0
        return count

    def get(self: Self, row, column) -> Cell:
        """Returns the cell at the given row and column indices"""
        return self.grid[row][column]
    
    def rows(self: Self) -> int:
        """Returns the number of rows in the map"""
        return self.__rows
    
    def columns(self: Self) -> int:
        """Returns the number of columns in the map"""
        return self.__columns
    
    def reset_sim(self: Self, posx: int, posy: int) -> None:
        """Resets all parameters inside the object to their default values, except for the grid itself.
        Takes as parameters the initial position of the player."""
        self.player_posx = posx
        self.player_posy = posy
        self.moves = 0
        self.orientation = Orientation.UP

    def until_next_obstacle(self: Self) -> Optional[Tuple[int, int]]:
        """Run the simulation until the player gets at the next obstacle.
        Returns None if the simulation has entered an infinite loop.
        Returns (-1,-1) if the player has exited the simulation.
        Returns the last valid coordinates of the player after hitting an obstacle. It also rotates the player."""

        # If the number of moves so far is bigger than the total number of cells in the grid, it is an infinite loop
        if self.moves > self.columns()*self.rows():
            return None

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
            # Increment the total number of moves
            self.moves += 1

            # If the coordinates of the next cell to be visited are not valid anymore, it means
            # we've exited the map and the simulation is done, return (-1,-1) to signify that
            if not self.valid_coords(self.player_posx + x_offset, self.player_posy + y_offset):
                return (-1,-1)
            
            # If we've hit an obstacle, don't advance any further, change orientation and return current coordinates
            if self.get(self.player_posx + x_offset, self.player_posy + y_offset).obstacle == True:
                self.orientation = self.orientation.rotate()
                return self.player_posx, self.player_posy
            
            # Otherwise, it means we still have some way to go, so increment x and y position with the offsets
            self.player_posx += x_offset
            self.player_posy += y_offset
    
    def step(self: Self):
        """Run the simulation for one step. When it hits an obstacle, it first rotates the player then returns.
        Returns None if the simulation is done (we've exited the map).
        Returns the last valid coordinates of the player."""

        # If the number of moves so far is bigger than the total number of cells in the grid, it is an infinite loop
        self.moves += 1
        if self.moves > self.columns()*self.rows():
            return None
        
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
            return [-1, -1]
        
        # If the new coordinates are an obstacle, rotate 90 degrees and don't change current coords
        if self.grid[new_coords[0]][new_coords[1]].obstacle == True:
            self.orientation = self.orientation.rotate()
            return [self.player_posx, self.player_posy]
        
        # If the coordinates are valid and there is no obstacle, set player coordinates to new_coords
        self.player_posx = new_coords[0]
        self.player_posy = new_coords[1]
        return new_coords
        
    def valid_coords(self: Self, x: int, y: int) -> bool:
        """Checks if x and y are valid coordinates in the current map"""
        if x >= 0 and y >= 0 and x < self.rows() and y < self.columns():
            return True
        return False
    
    def to_string(self: Self) -> str:
        """To string functionality for the board, useful for debugging. It should return back a string representation such that
        it coincides with the raw data in the given file."""
        result = ""
        for i in range(self.columns()):
            row = ""
            for j in range(self.rows()):
                if i == self.player_posx and j == self.player_posy:
                    row += "^"
                elif self.get(i, j).obstacle == True:
                    row += "#"
                elif self.get(i, j).obstacle == False:
                    row += "."
            result += row + "\n"
        return result

    
def load_file_into_array() -> List[List[str]]:
    """Writes the grid into a list of lists of strings that will later be parsed by the Map object"""
    text = []
    with open("ultra_test.txt", "r") as f:
        while line := f.readline():
            text.append(line.strip())

    return text

def run_simulation(grid: Map):
    """Given a map, run the simulation until the simulation ends.
    Returns 0 if the simulation ended successfully.
    Returns None if the simulation entered an infinite loop."""
    while True:
        step_result = grid.until_next_obstacle()
        if step_result == (-1, -1):
            return 0
        if step_result is None:
            return None
     

# Load the map data into the map object
raw_data = load_file_into_array()
map = Map(raw_data)

# Save initial player position
init_playerx = map.player_posx
init_playery = map.player_posy

# Start a timer to measure how long it took
start_time = time.process_time()
# Measure how many maps have entered an infinite loop
infinite_loop_count = 0
# Measure the total number of maps tested
total = 0

# For every x, y position on the map that is not an obstacle or the initial position of the player
for i in range(0, map.rows()):
    for j in range(0, map.columns()):
        total += 1

        if i == init_playerx and j == init_playery:
            continue
        if map.get(i, j).obstacle == True:
            continue

        # Set an obstacle at that position
        map.get(i, j).obstacle = True
        # Run the simulation and see if it enters an infinite loop
        sim_result = run_simulation(map)
        
        # If it does, increment the counter
        if sim_result is None:
            infinite_loop_count += 1
        
        # For every 1000th map tried, print a message with the progress
        if total % 1000 == 0:
            print(total, "grids tried so far out of", map.rows()*map.columns())
        
        # Set the cell back to being an empty cell and reset the parameters
        # for the next simulation
        map.get(i, j).obstacle = False
        map.reset_sim(init_playerx, init_playery)

# Print how many have entered infinite loops and how much time it took
end_time = time.process_time()
print("Time taken:", end_time - start_time, "s")
print(infinite_loop_count)