import copy

class Grid:
    def __init__(self,columns,rows):
        self.ymax = rows
        self.xmax = columns

        self.grid = []
        for y in range(rows):
            row = []
            for x in range(columns):
                row.append(Point(x,y))
            self.grid.append(row)

        self.routes = []
        self.walls = []
        self.sols = []

    def walk(self, pt):
        if not pt:
            return []
        else:
            return [s for s in [self.above(pt),self.below(pt),self.right(pt),self.left(pt)] if s is not False and s.status is not '0']

    def printgrid(self):
        for y in range(self.ymax):
            line = ""
            for x in range(self.xmax):
                line += str(self.grid[y][x].status)
            print line

    def printdist(self):
        for y in range(self.ymax):
            line = ""
            for x in range(self.xmax):
                line += str(self.grid[y][x].distance)+' '
            print line

    def getpt(self,pt):
        if (pt.x in range(self.xmax)) & (pt.y in range(self.ymax)):
            return self.grid[pt.y][pt.x]
        else:
            return False

    def status(self,pt):
        if (pt.x in range(self.xmax)) & (pt.y in range(self.ymax)):
            return self.grid[pt.y][pt.x].status
        else:
            return False

    def above(self,pt):
        if (pt.x in range(self.xmax)) & (pt.y+1 in range(self.ymax)):
            return self.grid[pt.y+1][pt.x]
        else:
            return False

    def below(self,pt):
        if (pt.x in range(self.xmax)) & (pt.y-1 in range(self.ymax)):
            return self.grid[pt.y-1][pt.x]
        else:
            return False

    def right(self,pt):
        if (pt.x+1 in range(self.xmax)) & (pt.y in range(self.ymax)):
            return self.grid[pt.y][pt.x+1]
        else:
            return False

    def left(self,pt):
        if (pt.x-1 in range(self.xmax)) & (pt.y in range(self.ymax)):
            return self.grid[pt.y][pt.x-1]
        else:
            return False

    def updatestatus(self,pt,ptype):
        if (pt.x in range(self.xmax)) & (pt.y in range(self.ymax)):
            if ptype in ['wall']:
                self.getpt(pt).status = '0'
            elif ptype in ['clear']:
                self.grid[pt.y][pt.x].status = ' '
            elif ptype in ['trace']:
                self.grid[pt.y][pt.x].status = 'x'
        else:
            return False
        return True

    def addroute(self,source,sinks):
        if (source.x not in range(self.xmax)) or (source.y not in range(self.ymax)):
            return False
        for sink in sinks:
            if (sink.x not in range(self.xmax)) or (source.y not in range(self.ymax)):
                return False
        self.routes.append([source,sinks])
        return True

    def addwall(self,wall):
        if (wall.x not in range(self.xmax)) or (wall.y not in range(self.ymax)):
            return False
        self.walls.append(wall)
        return True

    def setdistance(self,pt,d):
        if (pt.x in range(self.xmax)) & (pt.y in range(self.ymax)):
            self.getpt(pt).distance = d
            return True
        else:
            return False

    def cleardistance(self):
        for y in range(self.ymax):
            for x in range(self.xmax):
                self.grid[y][x].distance = 0

    def LeeMoore(self):
        for [source,sinks] in self.routes:
            for sink in sinks:
                self.updatestatus(sink,'trace')
            for sink in sinks:
                self.updatestatus(source,'trace')
                sol = []
                self.setdistance(source,1)
                fifo = [self.getpt(source)]
                done = False
                while (fifo != []) and not done:
                    current = fifo[0]
                    next = self.walk(current)
                    for point in next:
                        if point.match(sink) and not done:
                            done = True
                            self.setdistance(point,current.distance+1)
                    if not done:
                        for point in next:
                            if point.distance == 0:
                                fifo.append(point)
                                self.setdistance(point,current.distance+1)
                    fifo.pop(0)
                if done:
                    # TODO: this is where I select direction - better to move away from closest object, toward goal?
                    # TODO try to leave a gap between traces if possible, as well as walls
                    # TODO: intelligence here?
                    # TODO: momentum - continue in same direction 1-2 places if possible
                    current = self.getpt(sink)
                    while not current.match(self.getpt(source)):
                        next = self.walk(current)
                        for point in next:
                            if point.distance == current.distance-1:
                                if not point.match(source):
                                    sol.append(point)
                                current = point
                    for point in sol:
                        self.updatestatus(point,'trace')
                        self.sols.append(sol)

                self.printgrid()
                self.cleardistance()
            self.updatestatus(source, 'wall')
            for sink in sinks:
                self.updatestatus(sink, 'wall')
            for sol in self.sols:
                for point in sol:
                    self.updatestatus(point,'wall')


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = ' '
        self.distance = 0

    def __getitem__(self, item):
        return (self.x, self.y)[item]

    def match(self,pt):
        if (pt.x == self.x) & (pt.y == self.y):
            return True
        else:
            return False