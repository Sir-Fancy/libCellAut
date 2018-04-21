#!/usr/bin/env python3
from libCellAut import CellAut
import numpy as np
from blessings import Terminal
import curses
import time
import traceback

class Forest(CellAut):
    def firstframe(self):
        #Generate start field, init additional variables, override to change start state
        self.t = Terminal()
        for row in self.field:
            for cell in row:
                if np.random.random() < 0.01:
                   cell.stage("A")
    
    def tick(self):
        for row in self.field:
            for cell in row:
                if cell.val == "&" and cell.attr["life"] == 0:
                    cell.stage(" ") #maybe let other stuff happen after?
                elif cell.val == "&":
                    cell.attr["life"] -= 1
                elif cell.val == "A" and cell.adjacent("&") > 0:
                    cell.stage("&")
                    cell.attr["life"] = 3
                elif cell.val == " " and cell.adjacent("A") > 0 and np.random.random() < 0.10:
                    cell.stage("A")
                elif cell.val == "A" and np.random.random() < 0.005:
                    cell.stage("&")
                    cell.attr["life"] = 3
    
    def disp(self):
        global stdscr
        for row in self.field:
            for cell in row:
                if str(cell) == "&":
                    stdscr.addstr(cell.y, cell.x, str(cell), curses.color_pair(1))
                else:
                    stdscr.addstr(cell.y, cell.x, str(cell))
        stdscr.refresh()
               
        # for row in self.field:
        #     for cell in row:
        #         stdscr.addstr(cell.y, cell.x, "({},{})".format(cell.x, cell.y))
        #         stdscr.refresh()

def main():
    global stdscr
    stdscr = curses.initscr()
    curses.noecho()
    curses.start_color()
    curses.curs_set(False)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1) #add curses to libCellAut
    try:
        f = Forest(cols = 90, rows = 50, blank = " ", speed = 1)
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