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
        self.field[20,20].stage("#")
        self.field[21,21].stage("#")
        self.field[22,19].stage("#")
        self.field[22,20].stage("#")
        self.field[22,21].stage("#")

    
    def tick(self):
        for row in self.field:
            for cell in row:
                if cell.val == "#":
                    if cell.surrounding("#") < 2 or cell.surrounding("#") > 3:
                        cell.stage(self.blank)
                elif cell.val == self.blank:
                    if cell.surrounding("#") == 3:
                        cell.stage("#")
                    
                
    
    def disp(self):
        for row in self.field:
            for cell in row:
                    self.stdscr.addstr(cell.y, cell.x, str(cell), curses.color_pair(1))
        self.stdscr.refresh()

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