from cell import Cell
import random
import time

class Maze():
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None, 
            seed=None
            ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed != None:
            self._seed = random.seed(seed)
        self._cells = []

        self._create_cells()
    
    def _create_cells(self):
        for i in range(0, self._num_cols):
            cell_list = []
            for j in range(0, self._num_rows):
                cell_list.append(Cell(self._win))
            self._cells.append(cell_list)
        for i in range(0, self._num_cols):
            for j in range(0, self._num_rows):
                self._draw_cell(i, j)
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
    
    def _draw_cell(self, i, j):
        if self._win == None:
            return

        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        entrance.has_top_wall = False
        self._draw_cell(0, 0)
        
        exit = self._cells[self._num_cols - 1][self._num_rows - 1]
        exit.has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        # keep track of where we have been
        self._cells[i][j]._visited = True
        # go until we are done
        while True:
            # keep track of where we have not been
            to_visit = []

            # check the right side
            if i + 1 < self._num_cols and self._cells[i+1][j]._visited == False:
                to_visit.append([i+1, j])
            # check the left side
            if i - 1 >= 0 and self._cells[i-1][j]._visited == False:
                to_visit.append([i-1, j])
            # check the cell below
            if j + 1 < self._num_rows and self._cells[i][j+1]._visited == False:
                to_visit.append([i, j+1])
            # check the cell above
            if j - 1 >= 0 and self._cells[i][j-1]._visited == False:
                to_visit.append([i, j-1])
            
            # if we have no where to go break out of the recursion
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            # if we can go somewhere
            else:
                # pick a random place to go
                direction = random.randrange(len(to_visit))
                next_cell = to_visit[direction]
                # if that place is to the left
                if next_cell[0] < i:
                    self._cells[i][j].has_left_wall = False
                    self._cells[next_cell[0]][next_cell[1]].has_right_wall = False
                # if that place is to the right
                elif next_cell[0] > i:
                    self._cells[i][j].has_right_wall = False
                    self._cells[next_cell[0]][next_cell[1]].has_left_wall = False
                # if that place is above
                elif next_cell[1] < j:
                    self._cells[i][j].has_top_wall = False
                    self._cells[next_cell[0]][next_cell[1]].has_bottom_wall = False
                # if that place is below
                elif next_cell[1] > j:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[next_cell[0]][next_cell[1]].has_top_wall = False

            # go to the next place  
            self._break_walls_r(next_cell[0], next_cell[1])

    def _reset_cells_visited(self):
        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._cells[col][row]._visited = False
    
    def _solve_r(self, i, j):
        self._animate()

        # keep track of where we have been
        self._cells[i][j]._visited = True

        # if we reached the end
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        
        # check if we can traverse right
        if i + 1 < self._num_cols and self._cells[i][j].has_right_wall == False and self._cells[i+1][j]._visited == False:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j], True)
        # check if we can traverse left
        if i > 0 and self._cells[i][j].has_left_wall == False and self._cells[i-1][j]._visited == False:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j], True)
        # check if we can traverse up
        if j > 0 and self._cells[i][j].has_top_wall == False and self._cells[i][j-1]._visited == False:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], True)
        # check if we can traverse down
        if j + 1 < self._num_rows and self._cells[i][j].has_bottom_wall == False and self._cells[i][j+1]._visited == False:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1], True)
        
        return False

    def solve(self):
        return self._solve_r(0, 0)
        

            