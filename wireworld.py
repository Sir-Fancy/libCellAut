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

        for row in self.field:
            for cell in row:
                r = np.random.random()
                if r < 0.05:
                    cell.stage("x")
                elif r < 0.1:
                    cell.stage("o")
                elif r < 0.3:
                    cell.stage(".")

    def tick(self):
        for row in self.field:
            for cell in row:
                if cell.val == "x":
                    cell.stage("o")
                elif cell.val == "o":
                    cell.stage(".")
                elif cell.val == "." and cell.surrounding("x", wrap=self.wrap) in (1, 2):
                    cell.stage("x")

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
