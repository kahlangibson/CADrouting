from Tkinter import *
import Tkinter as tk
import Tkconstants, tkFileDialog
import Grid
from os import listdir
from os.path import isfile, join


class GridWindow:
    def __init__(self, parent):
        self.myParent = parent

        self.myContainer1 = tk.Frame(parent)
        self.myContainer1.pack()

        self.myCanvas = tk.Canvas(self.myContainer1)
        self.myCanvas.configure(borderwidth=0, highlightthickness=0,width=0,
                                height=0)

        self.cellwidth = 0
        self.cellheight = 0
        self.rect = {}
        self.text = {}
        self.fails = 0

    def delete(self):
        self.myCanvas.delete('all')
        self.myCanvas.configure(borderwidth=0, highlightthickness=0,width=0,
                                height=0)

    def draw_grid(self, rows, columns):
        bigger = max(columns, rows)
        self.cellwidth = 1000/bigger
        self.cellheight = 1000/bigger

        self.myCanvas = tk.Canvas(self.myContainer1)
        self.myCanvas.configure(borderwidth=0, highlightthickness=0,
                                width=self.cellheight*rows,
                                height=self.cellwidth*columns)
        self.myCanvas.pack(side=tk.RIGHT)

        for column in range(rows):
            for row in range(columns):
                x1 = column * self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[row, column] = self.myCanvas.create_rectangle(x1, y1, x2, y2, fill="white")

    def draw_walls(self, walls):
        for wall in walls:
            x1 = wall.x * self.cellwidth
            y1 = wall.y * self.cellheight
            x2 = x1 + self.cellwidth
            y2 = y1 + self.cellheight
            self.rect[wall.x, wall.y] = self.myCanvas.create_rectangle(x1, y1, x2, y2, fill="blue")

    def draw_routes(self, routes):
        colors = ["red", "yellow", "gray", "orange", "cyan", "pink", "green", "purple"]
        for num,[source,sinks] in enumerate(routes):
            x1 = source.x * self.cellwidth
            y1 = source.y * self.cellheight
            x2 = x1 + self.cellwidth
            y2 = y1 + self.cellheight
            self.rect[source.x, source.y] = self.myCanvas.create_rectangle(x1, y1, x2, y2, fill=colors[num])
            self.text[source.x, source.y] = self.myCanvas.create_text((x1+x2)/2, (y1+y2)/2, text=num+1)
            for sink in sinks:
                x1 = sink.x * self.cellwidth
                y1 = sink.y * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[sink.x, sink.y] = self.myCanvas.create_rectangle(x1, y1, x2, y2, fill=colors[num])
                self.text[sink.x, sink.y] = self.myCanvas.create_text((x1+x2)/2, (y1+y2)/2, text=num+1)

    def draw_sols(self, sols):
        for num,sol in enumerate([sol for sol in sols if sol is not False]):
            for pt in sol:
                x1 = pt.x * self.cellwidth + self.cellwidth/4
                y1 = pt.y * self.cellheight + self.cellheight/4
                x2 = x1 + self.cellwidth/2
                y2 = y1 + self.cellheight/2
                self.rect[pt.x, pt.y] = self.myCanvas.create_rectangle(x1, y1, x2, y2, fill='black')
        print "done " + str(len(sols)) + " routes"


def read_infile():
    global ggrid
    myapp.delete()
    filename = file.get()
    f = open('./benchmarks/'+filename, "r")  # opens file with name of filename

    #find size of grid
    [w,h] = [int(s) for s in f.readline().split()]

    myGrid = Grid.Grid(w,h)
    myapp.draw_grid(w, h)

    walls = []
    for _ in range(int(f.readline().split()[0])):
        walls.append([int(s) for s in f.readline().split()])
    for [x,y] in walls:
        myGrid.updatestatus(Grid.Point(x,y),'wall')
        myGrid.walls.append(Grid.Point(x,y))
    myapp.draw_walls(myGrid.walls)

    #number of wires to be created
    for num in range(int(f.readline().split()[0])):
        new_wire = f.readline().split()
        source = Grid.Point(int(new_wire[1]),int(new_wire[2]))
        myGrid.updatestatus(source,'wall')

        sinks = []
        for i in range(int(new_wire[0])-1):
            sinks.append(Grid.Point(int(new_wire[3+2*i]),int(new_wire[4+2*i])))
            myGrid.updatestatus(Grid.Point(int(new_wire[3+2*i]),int(new_wire[4+2*i])), 'wall')

        myGrid.addroute(source,sinks)

    myapp.draw_routes(myGrid.routes)

    f.close()
    myGrid.printgrid()
    ggrid = myGrid


def route():
    result = 0
    if var.get() == 'Lee-Moore':
        ggrid.LeeMoore()
        myapp.draw_sols(ggrid.sols)
    #if var.get() == 'LineProbe':
    #    result = LineProbe(wires)


## main ##
root = Tk()
root.lift()
root.attributes("-topmost", True)
#root.filename = tkFileDialog.askopenfilename(initialdir="./benchmarks/", title="Select File to Route")

myapp = GridWindow(root)

file = tk.StringVar(root)
# initial value
file.set('Choose File')
filenames = [f for f in listdir('./benchmarks/') if isfile(join('./benchmarks/', f))]
drop = tk.OptionMenu(root, file, *filenames)
drop.pack(side='left', padx=10, pady=10)
go = tk.Button(root, text="Choose File", command=read_infile)
go.pack(side='left', padx=20, pady=10)

var = tk.StringVar(root)
# initial value
var.set('Choose Routing Algorithm')
choices = ['Lee-Moore', 'Line Probe']
option = tk.OptionMenu(root, var, *choices)
option.pack(side='left', padx=10, pady=10)
button = tk.Button(root, text="Attempt Route", command=route)
button.pack(side='left', padx=20, pady=10)

root.mainloop()