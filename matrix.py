#!/usr/bin/env python3
from libCellAut import CellAut
import numpy as np
import curses
import time
import traceback
import sys
import random

class Fractal(CellAut):
    def firstframe(self):
        #Generate start field, init additional variables, override to change start state
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        self.chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        #self.field[-1,self.cols//2].stage("A")
    
        self.CELL_LIFE = 7

        for row in self.field:
            for cell in row:
                cell.attr["life"] = 0
    
    def tick(self):
        for row in self.field:
            for cell in row:
                if cell.val == " ":
                    if cell.get_rel(-1, 0) != " " or np.random.random() < 0.00005:
                        cell.stage(random.choice(self.chars))
                        cell.attr["life"] = self.CELL_LIFE
                else:
                    if cell.attr["life"] < 1:
                        cell.stage(" ")
                    else:
                        cell.attr["life"] -= 1
                    
                    
    
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