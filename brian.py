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
        
        self.fill = "#"
        ON_CHANCE = 0.2
        DEAD_CHANCE = 0.2
        
        curses.init_pair(1, -1, curses.COLOR_WHITE)
        
        for row in self.field:
            for cell in row:
                cell.attr["decay"] = False

        self.field[6,6].stage(self.fill) #       X
        self.field[6,7].stage(self.fill) #       ##X
        self.field[7,6].stage(self.fill) #      X##
        self.field[7,7].stage(self.fill) #       X
        
        self.field[5,6].attr["decay"] = True
        self.field[6,8].attr["decay"] = True
        self.field[7,5].attr["decay"] = True
        self.field[8,7].attr["decay"] = True
        
        for row in self.field:
            for cell in row:
                if cell.x > 50:
                    roll = np.random.random()
                    if roll < ON_CHANCE:
                        cell.stage(self.fill)
                    elif ON_CHANCE <= roll < DEAD_CHANCE:
                        cell.attr["decay"] = True
    
    def tick(self):
        for row in self.field:
            for cell in row:
                if cell.val == "#":
                    cell.stage(self.blank)
                    cell.attr["decay"] = True
                elif cell.val == self.blank and cell.surrounding(self.fill, wrap=self.wrap) == 2 and cell.attr["decay"] is False:
                    cell.stage(self.fill)
                elif cell.attr["decay"] == True:
                    cell.attr["decay"] = False
                
    def disp(self):
        for row in self.field:
            for cell in row:
                if cell.val == self.fill and cell.attr["decay"] == False:
                    self.stdscr.addstr(cell.y, cell.x, cell.val)
                elif cell.attr["decay"] == True:
                    self.stdscr.addstr(cell.y, cell.x, cell.val, curses.color_pair(1))
                else:
                    self.stdscr.addstr(cell.y, cell.x, cell.val)
        self.stdscr.refresh()


def main():
    try:
        f = Fractal(blank = " ", speed = .5)
        f.simulate()
    except KeyboardInterrupt:
        f.destroy_curses()
    except BaseException as e:
        f.destroy_curses()
        print(traceback.format_exc())
        
if __name__ == '__main__':
    main()