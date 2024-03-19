from tkinter import Tk, BOTH, Canvas
import time
import random


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.root.title = "titteli"
        self.canvas = Canvas()
        self.canvas.pack()
        self.run = False

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.run = True
        while self.run == True:
            self.redraw()

    def close(self):
        self.run = False
        self.root.protocol("wait_for_close", self.close)

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)
        canvas.pack()


class Cell:
    def __init__(self, p1: Point, p2: Point, win: Window):
        self.r_wall = True
        self.t_wall = True
        self.l_wall = True
        self.b_wall = True
        self.p_tr = Point(p2.x, p1.y)
        self.p_tl = p1
        self.p_bl = Point(p1.x, p2.y)
        self.p_br = p2
        self.win = win
        self.cen = Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
        self.visited = False

    def draw(self):

        if self.r_wall:
            win.draw_line(Line(self.p_br, self.p_tr), "black")
        else:
            win.draw_line(Line(self.p_br, self.p_tr), "white")
        if self.t_wall:
            win.draw_line(Line(self.p_tr, self.p_tl), "black")
        else:
            win.draw_line(Line(self.p_tr, self.p_tl), "white")
        if self.l_wall:
            win.draw_line(Line(self.p_tl, self.p_bl), "black")
        else:
            win.draw_line(Line(self.p_tl, self.p_bl), "white")
        if self.b_wall:
            win.draw_line(Line(self.p_bl, self.p_br), "black")
        else:
            win.draw_line(Line(self.p_bl, self.p_br), "white")

    def draw_move(self, to_cell, undo=False):
        if undo:
            col = "gray"
        else:
            col = "red"
        self.win.draw_line(Line(self.cen, to_cell.cen), col)


class Maze:
    def __init__(
            self,
            p1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win):
        self.cells = []
        self.win = win
        self.graph = {}
        for c in range(num_cols):
            col = []
            for r in range(num_rows):
                cel = Cell(
                    Point(p1.x + c * cell_size_x, p1.y + r * cell_size_y),
                    Point(p1.x + c * cell_size_x + cell_size_x, p1.y + r * cell_size_y + cell_size_y),
                    self.win)
                col.append(cel)
                self.graph[(c, r)] = set()
            self.cells.append(col)

    def draw_cells(self, ran=False):
        if ran:
            cal_lis = []
            for c in self.cells:
                for r in c:
                    cal_lis.append(r)
            for it in sorted(cal_lis, key=lambda x: random.random()):
                it.draw()
                self.animate()
            return

        for c in self.cells:
            for r in c:
                r.draw()
                self.animate()

    def animate(self):
        self.win.redraw()
        time.sleep(0.02)

    def break_entrance_and_exit(self):
        self.cells[0][0].l_wall = False
        self.cells[-1][-1].r_wall = False
        self.cells[0][0].draw()
        self.cells[-1][-1].draw()

    def break_walls(self):
        ra_c = range(len(self.cells))
        ra_r = range(len(self.cells[0]))

        i = []
        j = [(0, 0)]

        while j:
            cur = j[-1]
            i.append(cur)
            neib = [(cur[0] + 1, cur[1]), (cur[0], cur[1] - 1), (cur[0] - 1, cur[1]), (cur[0], cur[1] + 1)]
            valid = []
            for idx, c in enumerate(neib):
                if c[0] in ra_c and c[1] in ra_r and c not in i:
                    valid.append((idx, c))
            match len(valid):
                case 0:
                    j.pop()
                    continue
                case 1:
                    j.pop()
            rand = random.choice(valid)

            j.append(rand[1])
            print(rand[1])
            match rand[0]:

                case 0:
                    self.cells[cur[0]][cur[1]].r_wall = False
                    self.cells[rand[1][0]][rand[1][1]].l_wall = False
                case 1:
                    self.cells[cur[0]][cur[1]].t_wall = False
                    self.cells[rand[1][0]][rand[1][1]].b_wall = False
                case 2:
                    self.cells[cur[0]][cur[1]].l_wall = False
                    self.cells[rand[1][0]][rand[1][1]].r_wall = False
                case 3:
                    self.cells[cur[0]][cur[1]].b_wall = False
                    self.cells[rand[1][0]][rand[1][1]].t_wall = False

            self.graph[(cur[0], cur[1])].add((rand[1][0], rand[1][1]))
            self.graph[(rand[1][0], rand[1][1])].add((cur[0], cur[1]))

        self.draw_cells(True)

    def solve(self):
        visi = []
        solve = [False]

        def depth_first_search_r(visited, current_vertex, sol):
            if sol[0]: return
            visited.append(current_vertex)
            sor = sorted(self.graph[current_vertex])
            for s in sor:
                if sol[0]: return
                if s not in visited:
                    self.cells[current_vertex[0]][current_vertex[1]].visited = True
                    self.cells[current_vertex[0]][current_vertex[1]].draw_move(self.cells[s[0]][s[1]])
                    self.animate()
                    if s == (len(self.cells) - 1, len(self.cells[0]) - 1):
                        print("Solved!!!")
                        sol[0] = True
                        return
                    depth_first_search_r(visited, s, sol)
                    if sol[0]: return

                    self.cells[s[0]][s[1]].draw_move(self.cells[current_vertex[0]][current_vertex[1]], True)
                    self.animate()

        depth_first_search_r(visi, (0, 0), solve)


if __name__ == '__main__':
    win = Window(1000, 1000)

    win.redraw()

    maz = Maze(Point(15, 15), 12, 18, 20, 20, win)
    maz.draw_cells()
    maz.break_entrance_and_exit()
    maz.break_walls()
    maz.solve()

    win.wait_for_close()
