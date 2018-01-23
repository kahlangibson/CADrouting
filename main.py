from Tkinter import *
import Tkinter as tk
import Tkconstants, tkFileDialog
import copy


class GridWindow:
    def __init__(self, parent):
        self.myParent = parent

        self.myContainer1 = tk.Frame(parent)
        self.myContainer1.pack()

        self.cellwidth = 0
        self.cellheight = 0
        self.rect = {}
        self.text = {}

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

    def draw_walls(self, coord):
        for column,row in coord:
            x1 = column * self.cellwidth
            y1 = row * self.cellheight
            x2 = x1 + self.cellwidth
            y2 = y1 + self.cellheight
            self.rect[row, column] = self.myCanvas.create_rectangle(x1, y1, x2, y2, fill="blue")

    def draw_wires(self, wires):
        colors = ["red", "yellow", "gray", "orange", "cyan", "pink", "green", "purple"]
        for num,[source,sinks] in enumerate(wires):
            x1 = source[0] * self.cellwidth
            y1 = source[1] * self.cellheight
            x2 = x1 + self.cellwidth
            y2 = y1 + self.cellheight
            self.rect[source[0], source[1]] = self.myCanvas.create_rectangle(x1, y1, x2, y2, fill=colors[num])
            self.text[source[0], source[1]] = self.myCanvas.create_text((x1+x2)/2, (y1+y2)/2, text=num+1)
            for sink in sinks:
                x1 = sink[0] * self.cellwidth
                y1 = sink[1] * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[sink[0], sink[1]] = self.myCanvas.create_rectangle(x1, y1, x2, y2, fill=colors[num])
                self.text[sink[0], sink[1]] = self.myCanvas.create_text((x1+x2)/2, (y1+y2)/2, text=num+1)

    def draw_sols(self, sols):
        for (x,y) in sols:
            x1 = x * self.cellwidth
            y1 = y * self.cellheight
            x2 = x1 + self.cellwidth
            y2 = y1 + self.cellheight
            self.rect[x, y] = self.myCanvas.create_rectangle(x1, y1, x2, y2, fill="black")


def read_infile(filename):
    f = open(filename, "r")  # opens file with name of filename

    #find size of grid
    [w,h] = [int(s) for s in f.readline().split()]

    grid = []
    for _ in range(h):
        line = []
        for _ in range(w):
            line.append(' ')
        grid.append(line)

    myapp.draw_grid(w, h)

    walls = []
    for _ in range(int(f.readline().split()[0])):
        #print f.readline().split()
        walls.append([int(s) for s in f.readline().split()])
    for [x,y] in walls:
        grid[y][x] = '0'
    myapp.draw_walls(walls)

    #number of wires to be created
    wires = []
    for num in range(int(f.readline().split()[0])):
        new_wire = []
        sink = []
        for s in f.readline().split():
            new_wire.append(int(s))

        source = (new_wire[1],new_wire[2])
        grid[new_wire[2]][new_wire[1]] = -1*(num+1)

        for i in range(new_wire[0]-1):
            sink.append((new_wire[3+2*i],new_wire[4+2*i]))
            grid[new_wire[4+2*i]][new_wire[3+2*i]] = -1*(num+1)

        wires.append((source,sink))

    myapp.draw_wires(wires)
    #print wires

    f.close()
    return wires, grid, w, h

def route():
    result = 0
    if var.get() == 'Lee-Moore':
        result = LeeMoore(wires,grid)
    #if var.get() == 'LineProbe':
    #    result = LineProbe(wires)

def LeeMoore(wires,grid):
    sols = []
    for source,sinks in wires:
        for sink in sinks:
            gtemp = copy.deepcopy(grid)
            #TODO: repopulate grid with solutions of previous routes
            #Dont really need to bother with sols on same node
            coordList = []
            coordList.append((source,1))
            done = False
            while (coordList != []) & (done != True):
                coordList,gtemp,done = LMRoute(coordList,sink,gtemp,done)
            if(done == True):
                #populate list of coords to draw solution
                sol = []
                current = sink
                val = gtemp[sink[1]][sink[0]]
                while val > 2:
                    (x,y) = current
                    #TODO: this is where I select direction - better to move away from closest object?
                    #TODO: intelligence here?
                    if(gtemp[y-1][x] == val-1):
                        current = (x, y-1)
                        sol.append(current)
                        val -= 1
                    elif (gtemp[y+1][x] == val - 1):
                        current = (x, y+1)
                        sol.append(current)
                        val -= 1
                    elif (gtemp[y][x+1] == val - 1):
                        current = (x+1, y)
                        sol.append(current)
                        val -= 1
                    elif (gtemp[y][x-1] == val - 1):
                        current = (x-1, y)
                        sol.append(current)
                        val -= 1
                myapp.draw_sols(sol)
                sols.append(sol)

def LMRoute(coordList,sink,gtemp,done):
    #print coordList[0]
    ((x,y),count) = coordList[0]
    count += 1
    changes = []
    #above = [x,y-1]
    if (x == sink[0]) & (y-1 == sink[1]):
        #found location! write and return
        done = True
        gtemp[y-1][x] = count
        #print x, y-1
        return coordList, gtemp, done
    elif y>0:
        if (gtemp[y-1][x] == ' '):
            #empty and valid location, append to coordList
            changes.append([x,y-1])
            coordList.append(((x,y-1),count))
    #below = [x,y+1]
    if (x == sink[0]) & (y+1 == sink[1]):
        #found location! write and return
        done = True
        gtemp[y+1][x] = count
        #print x, y+1
        return coordList, gtemp, done
    elif y+1<h:
        if (gtemp[y+1][x] == ' '):
            #empty and valid location, append to coordList
            changes.append([x,y+1])
            coordList.append(((x,y+1),count))
    #right = [x+1,y]
    if (x+1 == sink[0]) & (y == sink[1]):
        #found location! write and return
        done = True
        gtemp[y][x+1] = count
        #print x+1, y
        return coordList, gtemp, done
    elif x+1<w:
        if (gtemp[y][x+1] == ' '):
            #empty and valid location, append to coordList
            changes.append([x+1,y])
            coordList.append(((x+1,y),count))
    #right = [x-1,y]
    if (x-1 == sink[0]) & (y == sink[1]):
        #found location! write and return
        done = True
        gtemp[y][x-1] = count
        #print x-1, y
        return coordList, gtemp, done
    elif x>0:
        if (gtemp[y][x-1] == ' '):
            #empty and valid location, append to coordList
            changes.append([x-1,y])
            coordList.append(((x-1,y),count))
    for [x,y] in changes:
        gtemp[y][x] = count
    coordList.pop(0)
    return coordList, gtemp, done

## main ##
root = Tk()
root.lift()
root.attributes("-topmost", True)
root.filename = tkFileDialog.askopenfilename(initialdir="./benchmarks/", title="Select File to Route")

myapp = GridWindow(root)
wires,grid,w,h = read_infile(root.filename)

var = tk.StringVar(root)

# initial value
var.set('Choose Routing Algorithm')
choices = ['Lee-Moore', 'Line Probe']
option = tk.OptionMenu(root, var, *choices)
option.pack(side='left', padx=10, pady=10)
button = tk.Button(root, text="Attempt Route", command=route)
button.pack(side='left', padx=20, pady=10)

root.mainloop()