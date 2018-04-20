#!/usr/bin/env python3
import time
import numpy as np

class CellAut(object):
    def __init__(self, rows = 20, cols = 40, blank = " ", speed = 1.0):
        self.rows = rows
        self.cols = cols
        self.blank = blank
        self.speed = speed
        self.field = np.empty((rows, cols), object)
        for y in range(len(self.field[0])):
            for x in range(len(self.field)):
                self.field[x,y] = CellAut.Cell(self, x, y, self.blank)
        
        #somewhere at the end of a frame needs to be self.field[:] = self.stage[:]
        
    def firstframe(self):
        #Generate start field, init additional variables, override to change start state
        #self.i = 0
        for row in self.field:
            for cell in row:
                if np.random.random() < 0.2:
                    cell.val = "1"
        
    def simulate(self):
        starttime = time.time()
        self.firstframe()
        self.commit()
        while True:
            self.disp()
            self.tick()
            self.commit()
            time.sleep(self.speed - ((time.time() - starttime) % self.speed))

    
    def tick(self):
        for row in self.field:
            for cell in row:
                cell.stage(str(int(str(cell)) + 1))
    
    def commit(self):
        for row in self.field:
            for cell in row:
                cell.commit()
    
    def disp(self):
        #TODO use ncurses
        s = ""
        for row in self.field:
            for cell in row:
                s += str(cell)
            s += "\n"
        print(s)
                
    class Cell(object):
        def __init__(self, parent, x, y, val, attr = {}):
            self.parent = parent
            self.x = x
            self.y = y
            self.val = val
            self.staged = val
            self.attr = attr
            
        def __str__(self):
            return self.val

        def adjacent(self, search):
            count = 0
            for i in [(self.x-1, self.y), (self.x+1, self.y), (self.x, self.y-1), (self.x, self.y+1)]:
                try:
                    v = str(self.parent.field[i])
                except IndexError:
                    continue
                if v == search:
                    count += 1
            return count

        def stage(self, v):
            self.staged = v
        
        def commit(self):
            self.val = self.staged

if __name__ == '__main__':
    test = CellAut(blank = "0")
    test.simulate()
    