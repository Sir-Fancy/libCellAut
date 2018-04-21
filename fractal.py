#!/usr/bin/env python3
from libCellAut import CellAut
import numpy as np
import curses
import time
import traceback

class Fractal(CellAut):
    def firstframe(self):
        #Generate start field, init additional variables, override to change start state
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        self.field[49,40].stage("A")
    
    def tick(self):
        for row in self.field:
            for cell in row:
                if cell.adjacent("A") == 1:
                    cell.stage("A") 
    
    def disp(self):
        for row in self.field:
            for cell in row:
                    self.stdscr.addstr(cell.y, cell.x, str(cell), curses.color_pair(1))
        self.stdscr.refresh()

def main():
    try:
        f = Fractal(cols = 90, rows = 50, blank = " ", speed = 0.5)
        f.simulate()
    except KeyboardInterrupt:
        curses.echo()
        curses.endwin()
        curses.curs_set(True)
    except BaseException as e:
        curses.echo()
        curses.endwin()
        curses.curs_set(True)
        print(traceback.format_exc())
if __name__ == '__main__':
    main()