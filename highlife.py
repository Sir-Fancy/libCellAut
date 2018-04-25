#!/usr/bin/env python3
from libCellAut import CellAut
import numpy as np
import curses
import time
import traceback
import sys

class Fractal(CellAut):
    def firstframe(self):
        #Generate start field, init additional variables, override to change start state
        args = sys.argv
        self.wrap = False
        if "--wrap" in args:
            self.wrap = True
        
        if "glider" in args:
            self.field[20,20].stage("#")
            self.field[21,21].stage("#")
            self.field[22,19].stage("#")
            self.field[22,20].stage("#")
            self.field[22,21].stage("#")
        else:
            for row in self.field:
                for cell in row:
                    if np.random.random() < 0.1:
                        cell.stage("#")
    
    def tick(self):
        for row in self.field:
            for cell in row:
                if cell.val == "#":
                    if cell.surrounding("#", wrap=self.wrap) < 2 or cell.surrounding("#", wrap=self.wrap) > 3:
                        cell.stage(self.blank)
                elif cell.val == self.blank:
                    if cell.surrounding("#", wrap=self.wrap) in [3,6]:
                        cell.stage("#")

def main():
    try:
        f = Fractal(blank = " ", speed = 0.2)
        f.simulate()
    except KeyboardInterrupt:
        f.destroy_curses()
    except BaseException as e:
        f.destroy_curses()
        print(traceback.format_exc())
        
if __name__ == '__main__':
    main()