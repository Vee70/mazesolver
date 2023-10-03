import tkinter as tk


class Window:
    def __init__(self, width, height):
        self._bg_color = 'white'
        self.__root = tk.Tk()
        self.__root.title('Maze Solver')
        self.__root.protocol('WM_DELETE_WINDOW', self.close)
        self.__canvas = tk.Canvas(
            self.__root,
            height=height,
            width=width,
            background=self._bg_color,
        )
        self.__canvas.pack(fill=tk.BOTH, expand=1)
        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x,
            self.p1.y,
            self.p2.x,
            self.p2.y,
            fill=fill_color,
            width=2,
        )
        canvas.pack(fill=tk.BOTH, expand=1)


class Cell:
    def __init__(self, x1, y1, x2, y2, window):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._window = window
        self.has_left = True
        self.has_right = True
        self.has_top = True
        self.has_bottom = True
        self.visited = False

    def draw(self):
        line_left = Line(
            Point(self._x1, self._y1),
            Point(self._x1, self._y2),
        )
        color = 'black' if self.has_left else self._window._bg_color
        self._window.draw_line(line_left, color)

        line_right = Line(
            Point(self._x2, self._y1),
            Point(self._x2, self._y2),
        )
        color = 'black' if self.has_right else self._window._bg_color
        self._window.draw_line(line_right, color)

        line_top = Line(
            Point(self._x1, self._y1),
            Point(self._x2, self._y1),
        )
        color = 'black' if self.has_top else self._window._bg_color
        self._window.draw_line(line_top, color)

        line_bottom = Line(
            Point(self._x1, self._y2),
            Point(self._x2, self._y2),
        )
        color = 'black' if self.has_bottom else self._window._bg_color
        self._window.draw_line(line_bottom, color)

    def _get_mid_point(self):
        x_mid = self._x1 + (self._x2 - self._x1) / 2
        y_mid = self._y1 + (self._y2 - self._y1) / 2
        return x_mid, y_mid

    def draw_move(self, to_cell, undo=False):
        color = 'gray' if undo else 'red'
        x1_mid, y1_mid = self._get_mid_point()
        x2_mid, y2_mid = to_cell._get_mid_point()
        line = Line(
            Point(x1_mid, y1_mid),
            Point(x2_mid, y2_mid)
        )
        self._window.draw_line(line, color)
