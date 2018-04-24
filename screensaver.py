#!/usr/bin/env python3
from libCellAut import CellAut
import numpy as np
import curses
import time
import traceback
import sys

class Screensaver(CellAut):
    def firstframe(self):
        #Generate start field, init additional variables, override to change start state
        curses.init_pair(1, curses.COLOR_GREEN, -1)

        self.CELL_LIFE = 8
        self.DECAY_TIME = 40

        self.field[-1,0].stage("#")
        for row in self.field:
            for cell in row:
                cell.attr["life"] = self.CELL_LIFE
                cell.attr["decay"] = 0
        
    def tick(self):
        for row in self.field:
            for cell in row:
                if cell.val == " " and cell.attr["decay"] > 0:
                    cell.attr["decay"] -= 1
                elif cell.val == "#" and cell.attr["life"] <= 0:
                    cell.stage(" ")
                    cell.attr["decay"] = self.DECAY_TIME
                elif cell.val == "#": #age
                    cell.attr["life"] -= 1
                elif cell.val == " " and cell.surrounding("#") == 1:
                    cell.stage("#")
                    cell.attr["life"] = self.CELL_LIFE
    
    def disp(self):
        for row in self.field:
            for cell in row:
                    self.stdscr.addstr(cell.y, cell.x, cell.val, curses.color_pair(1))
        self.stdscr.refresh()

def main():
    try:
        f = Screensaver(blank = " ", speed = 0.1)
        f.simulate()
    except KeyboardInterrupt:
        f.destroy_curses()
    except BaseException as e:
        f.destroy_curses()
        print(traceback.format_exc())
        
if __name__ == '__main__':
    main()