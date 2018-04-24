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
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        self.field[-1,self.cols//2].stage("A")
    
    def tick(self):
        for row in self.field:
            for cell in row:
                if cell.adjacent("A") == 1:
                    cell.stage("A") 
    
    def disp(self):
        for row in self.field:
            for cell in row:
                    self.stdscr.addstr(cell.y, cell.x, cell.val, curses.color_pair(1))
        self.stdscr.refresh()

def main():
    try:
        f = Fractal(blank = " ", speed = 0.1)
        f.simulate()
    except KeyboardInterrupt:
        f.destroy_curses()
    except BaseException as e:
        f.destroy_curses()
        print(traceback.format_exc())
        
if __name__ == '__main__':
    main()