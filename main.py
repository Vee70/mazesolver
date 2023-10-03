from window import *
from maze import *


window = Window(800, 800)

maze = Maze(25, 25, 15, 15, 50, 50, window)
maze._break_entrace_and_exit()
maze._break_walls_r(0, 0)
maze._reset_cells_visited()
maze.solve()

window.wait_for_close()
