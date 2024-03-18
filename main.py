from tkinter import Tk, BOTH, Canvas


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
    def __init__(self, p1:Point, p2:Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas:Canvas, fill_color):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)
        canvas.pack()





if __name__ == '__main__':
    win = Window(800, 600)

    l1 = Line(Point(10,10), Point(50, 10))
    l2 = Line(Point(50,10), Point(40, 20))
    l3 = Line(Point(40,20), Point(90, 90))
    win.draw_line(l1, "black")
    win.draw_line(l2, "red")
    win.draw_line(l3, "black")
    win.wait_for_close()