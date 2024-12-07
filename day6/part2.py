from typing import List, Self
from enum import Enum
import time

class Cell:
    def __init__(self: Self, isVisited: bool, isObstacle: bool):
        self.visited = isVisited
        self.obstacle = isObstacle

class Orientation(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def rotate(self: Self) -> Self:
        if self == Orientation.UP:
            return Orientation.RIGHT
        elif self == Orientation.DOWN:
            return Orientation.LEFT
        elif self == Orientation.LEFT:
            return Orientation.UP
        else:
            return Orientation.DOWN

class Map:
    def __init__(self: Self, lines: List[List[str]] = None) -> None:
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
        count = 0
        for line in self.grid:
            for cell in line:
                count += 1 if cell.visited == True else 0
        return count

    def get(self: Self, row, column) -> Cell:
        return self.grid[row][column]
    
    def columns(self: Self) -> int:
        return self.__columns
    
    def rows(self: Self) -> int:
        return self.__rows
    
    def reset_sim(self: Self, posx: int, posy: int) -> None:
        self.player_posx = posx
        self.player_posy = posy
        self.moves = 0
        self.orientation = Orientation.UP

    def until_next_obstacle(self: Self):
        if self.moves > self.columns()*self.rows():
            return None

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
            self.moves += 1
            if not self.valid_coords(self.player_posx + x_offset, self.player_posy + y_offset):
                return (-1,-1)
            if self.get(self.player_posx + x_offset, self.player_posy + y_offset).obstacle == True:
                self.orientation = self.orientation.rotate()
                return self.player_posx, self.player_posy
            
            self.player_posx += x_offset
            self.player_posy += y_offset
    
    def step(self: Self):
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
        # and mark the node as visited
        self.player_posx = new_coords[0]
        self.player_posy = new_coords[1]
        self.get(self.player_posx, self.player_posy).visited = True
        return new_coords
        
    def valid_coords(self: Self, x: int, y: int) -> bool:
        if x >= 0 and y >= 0 and x < self.rows() and y < self.columns():
            return True
        return False
    
    def to_string(self: Self) -> str:
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
    text = []
    with open("ultra_test.txt", "r") as f:
        while line := f.readline():
            text.append(line.strip())

    return text

def run_simulation(grid: Map):
    while True:
        step_result = grid.until_next_obstacle()
        if step_result == (-1, -1):
            return 0
        if step_result is None:
            return None
     
    
raw_data = load_file_into_array()
map = Map(raw_data)

init_playerx = map.player_posx
init_playery = map.player_posy
start_time = time.process_time()
elapsed_time_count = 0
total = 0

for i in range(0, map.rows()):
    for j in range(0, map.columns()):
        total += 1

        if i == init_playerx and j == init_playery:
            continue
        if map.get(i, j).obstacle == True:
            continue

        map.get(i, j).obstacle = True
        sim_result = run_simulation(map)
        if sim_result is None:
            elapsed_time_count += 1
            
        if total % 1000 == 0:
            print(total, "grids tried so far out of", map.rows()*map.columns())
        
        map.get(i, j).obstacle = False
        map.reset_sim(init_playerx, init_playery)

end_time = time.process_time()
print("Time taken:", end_time - start_time, "s")
print(elapsed_time_count)