import time
import random

from window import *


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
        seed=None,
    ):
        if seed:
            random.seed(seed)

        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = list()

        self._create_cells()

    def _create_cells(self):
        for i_col in range(self._num_cols):
            cells = list()
            for j_row in range(self._num_rows):
                # update (x, y) position of the next cell
                x1 = self._x1 + i_col * self._cell_size_x
                y1 = self._y1 + j_row * self._cell_size_y
                x2 = x1 + self._cell_size_x
                y2 = y1 + self._cell_size_y
                cells.append(Cell(x1, y1, x2, y2, self._win))
            self._cells.append(cells)
        if self._win:
            for i in range(self._num_cols):
                for j in range(self._num_rows):
                    self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.02)

    def _break_entrace_and_exit(self):
        col_start, row_start = 0, 0
        col_end, row_end = self._num_cols-1, self._num_rows-1
        self._cells[col_start][row_start].has_top = False
        self._cells[col_end][row_end].has_bottom = False
        self._draw_cell(col_start, row_start)
        self._draw_cell(col_end, row_end)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visited = []
            # left cell
            if i-1 >= 0 and not self._cells[i-1][j].visited:
                to_visited.append((i-1, j))
            # right cell
            if i+1 < self._num_cols and not self._cells[i+1][j].visited:
                to_visited.append((i+1, j))
            # top cell
            if j-1 >= 0 and not self._cells[i][j-1].visited:
                to_visited.append((i, j-1))
            # bottom cell
            if j+1 < self._num_rows and not self._cells[i][j+1].visited:
                to_visited.append((i, j+1))

            if not to_visited:
                self._draw_cell(i, j)
                return

            i_new, j_new = random.choice(to_visited)

            # left cell
            if i_new == i-1:
                self._cells[i][j].has_left = False
                self._cells[i-1][j].has_right = False
            # right cell
            if i_new == i+1:
                self._cells[i][j].has_right = False
                self._cells[i+1][j].has_left = False
            # top cell
            if j_new == j-1:
                self._cells[i][j].has_top = False
                self._cells[i][j-1].has_bottom = False
            # botom cell
            if j_new == j+1:
                self._cells[i][j].has_bottom = False
                self._cells[i][j+1].has_top = False

            self._break_walls_r(i_new, j_new)

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        curr_cell = self._cells[i][j]
        self._animate()
        curr_cell.visited = True
        if i == self._num_cols-1 and j == self._num_rows-1:
            return True

        if i-1 >= 0 and not self._cells[i-1][j].visited and not curr_cell.has_left:
            curr_cell.draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            else:
                curr_cell.draw_move(self._cells[i-1][j], undo=True)

        if i+1 < self._num_cols and not self._cells[i+1][j].visited and not curr_cell.has_right:
            curr_cell.draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            else:
                curr_cell.draw_move(self._cells[i+1][j], undo=True)

        if j-1 >= 0 and not self._cells[i][j-1].visited and not curr_cell.has_top:
            curr_cell.draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            else:
                curr_cell.draw_move(self._cells[i][j-1], undo=True)

        if j+1 < self._num_rows and not self._cells[i][j+1].visited and not curr_cell.has_bottom:
            curr_cell.draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            else:
                curr_cell.draw_move(self._cells[i][j+1], undo=True)

        return False
