from unittest import TestCase
from os import listdir
from os.path import isfile, join
import Grid


def generate_test_grids():
    grids = []
    filenames = [f for f in listdir('./benchmarks/') if isfile(join('./benchmarks/', f))]
    for filename in filenames:
        f = open('./benchmarks/'+filename, "r")  # opens file with name of filename
        grids.append(Grid.Grid(f))
    filenames = [f for f in listdir('../benchmarks/') if isfile(join('../benchmarks/', f))]
    for filename in filenames:
        f = open('../benchmarks/'+filename, "r")  # opens file with name of filename
        grids.append(Grid.Grid(f))
    return grids


class TestGrid(TestCase):

    def test_walk(self):
        for grid in generate_test_grids():
            # iterate points
            for x in range(grid.xmax):
                for y in range(grid.ymax):
                    num = 0
                    for point in [grid.above(Grid.Point(x,y)),grid.below(Grid.Point(x,y)),grid.right(Grid.Point(x,y)),grid.left(Grid.Point(x,y))]:
                        if point is not None:
                            if point.status is not '0':
                                num += 1
                    if x==0 and y==0:
                        self.assertEqual(len(grid.walk(Grid.Point(x,y))),num,"FAIL on minimum corner")
                    elif x==grid.xmax-1 and y==grid.ymax-1:
                        self.assertEqual(len(grid.walk(Grid.Point(x,y))),num,"FAIL on maximum corner")
                    elif x==0 or y==0:
                        self.assertEqual(len(grid.walk(Grid.Point(x,y))),num,"FAIL on minimum edge")
                    elif x == grid.xmax - 1 or y == grid.ymax - 1:
                        self.assertEqual(len(grid.walk(Grid.Point(x,y))),num,"FAIL on maximum edge")
                    else:
                        self.assertEqual(len(grid.walk(Grid.Point(x,y))),num,"FAIL internal point")
            # try point outside range
            x = 2 * grid.xmax
            y = 2 * grid.ymax
            self.assertEqual(len(grid.walk(Grid.Point(x, y))), 0, "FAIL external point")

    def test_getpt(self):
        for grid in generate_test_grids():
            for x in range(grid.xmax):
                for y in range(grid.ymax):
                    self.assertEqual(x,grid.getpt(Grid.Point(x,y)).x,"FAIL getting matching point coordinates")
                    self.assertEqual(y,grid.getpt(Grid.Point(x,y)).y,"FAIL getting matching point coordinates")
            # try point outside range
            x = grid.xmax
            y = 2 * grid.ymax
            self.assertIsNone(grid.getpt(Grid.Point(x,y)),"FAIL returned point that should not exist")
            x = 2 * grid.xmax
            y = grid.ymax
            self.assertIsNone(grid.getpt(Grid.Point(x,y)),"FAIL returned point that should not exist")
            x = 2 * grid.xmax
            y = 2 * grid.ymax
            self.assertIsNone(grid.getpt(Grid.Point(x,y)),"FAIL returned point that should not exist")
            x = -2 * grid.xmax
            y = -2 * grid.ymax
            self.assertIsNone(grid.getpt(Grid.Point(x,y)),"FAIL returned point that should not exist")

    def test_updatestatus(self):
        for grid in generate_test_grids():
            for x in range(grid.xmax):
                for y in range(grid.ymax):
                    status = grid.status(Grid.Point(x,y))
                    self.assertEqual(grid.updatestatus(Grid.Point(x,y), 0),False)
                    self.assertEqual(grid.status(Grid.Point(x,y)),status)
                    self.assertEqual(grid.updatestatus(Grid.Point(x,y), 'wall'),True)
                    self.assertEqual(grid.status(Grid.Point(x,y)),'0')
                    self.assertEqual(grid.updatestatus(Grid.Point(x,y), 'trace'),True)
                    self.assertEqual(grid.status(Grid.Point(x,y)),'x')
                    self.assertEqual(grid.updatestatus(Grid.Point(x,y), 'clear'),True)
                    self.assertEqual(grid.status(Grid.Point(x,y)),' ')

    def test_cleardistance(self):
        for grid in generate_test_grids():
            for x in range(grid.xmax):
                for y in range(grid.ymax):
                    grid.setdistance(Grid.Point(x,y),50)

            for x in range(grid.xmax):
                for y in range(grid.ymax):
                    self.assertEqual(grid.getpt(Grid.Point(x,y)).distance, 50, "FAIL distance not set")

            grid.cleardistance()
            for x in range(grid.xmax):
                for y in range(grid.ymax):
                    self.assertEqual(grid.getpt(Grid.Point(x,y)).distance, 0, "FAIL distance not reset")
