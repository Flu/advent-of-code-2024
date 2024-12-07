from typing import List, Self
from enum import Enum

class Cell:
    def __init__(self, isVisited: bool, isObstacle: bool):
        self.visited = isVisited
        self.obstacle = isObstacle


class Orientation(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def rotate(self) -> None:
        if self == Orientation.UP:
            return Orientation.RIGHT
        elif self == Orientation.DOWN:
            return Orientation.LEFT
        elif self == Orientation.LEFT:
            return Orientation.UP
        else:
            return Orientation.DOWN

class Grid:
    def __init__(self, lines: List[List[str]]):
        self.grid = []
        self.player_posx = 0
        self.player_posy = 0
        self.orientation = Orientation.UP
        self.moves = 0

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

    def how_many_visited(self):
        count = 0
        for line in self.grid:
            for cell in line:
                count += 1 if cell.visited == True else 0
        return count

    def get(self, row, column) -> Cell:
        return self.grid[row][column]
    
    def columns(self):
        return self.__columns
    
    def rows(self):
        return self.__rows
    
    def reset_sim(self: Self, posx: int, posy: int) -> None:
        self.player_posx = posx
        self.player_posy = posy
        self.orientation = Orientation.UP
        self.moves = 0
        for i in range(grid.rows()):
            for j in range(grid.columns()):
                self.grid[i][j].visited = False
    
    def until_next_obstacle(self: Self):
        if self.moves > self.rows()*self.columns():
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
            self.get(self.player_posx, self.player_posy).visited = True
            if not self.valid_coords(self.player_posx + x_offset, self.player_posy + y_offset):
                return (-1,-1)
            if self.get(self.player_posx + x_offset, self.player_posy + y_offset).obstacle == True:
                self.orientation = self.orientation.rotate()
                return self.player_posx, self.player_posy
            
            self.player_posx += x_offset
            self.player_posy += y_offset
    
    def step(self):
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
        
    def valid_coords(self, x:int, y:int) -> bool:
        if x < 0 or x >= self.columns():
            return False
        if y < 0 or y >= self.rows():
            return False
        return True
    
def load_file_into_array():
    text = []
    with open("ultra_test.txt", "r") as f:
        while line := f.readline():
            text.append(line.strip())

    return text

def run_simulation(grid: Grid):
    while result := grid.until_next_obstacle():
        if result == (-1,-1):
            break 
        if result is None:
            return 0
    return grid.how_many_visited()


raw_data = load_file_into_array()
grid = Grid(raw_data)

max_visited = 0
max_x = 0
max_y = 0

for i in range(grid.rows()):
    for j in range(grid.columns()):
        grid.reset_sim(i, j)
        visits = run_simulation(grid)
        if visits > max_visited:
            max_visited = visits
            max_x = i
            max_y = j
    print("Finished row", i, "/", grid.rows())
        

print("Max visited:", max_visited, max_x, max_y)