#!/usr/bin/env python3
from libCellAut import CellAut
import numpy as np
import curses
import time
import traceback

class Forest(CellAut):
    def firstframe(self):
        #Generate start field, init additional variables, override to change start state
        curses.init_pair(1, curses.COLOR_RED, -1)
        
        self.GROWTH_CHANCE = 0.10
        self.FIRE_CHANCE = 0.005
        self.FIRE_LIFE = 2
        
        for row in self.field:
            for cell in row:
                if np.random.random() < 0.01:
                   cell.stage("A")
    
    def tick(self):
        for row in self.field:
            for cell in row:
                if cell.val == "&" and cell.attr["life"] <= 0: #if fire life over, die
                    cell.stage(" ")
                elif cell.val == "&": #age fire
                    assert cell.attr["life"] > 0
                    cell.attr["life"] -= 1
                elif cell.val == "A" and (cell.adjacent("&") > 0 or (np.random.random() < self.FIRE_CHANCE)): #if adjacent to fire or random chance, enflame
                    cell.stage("&")
                    cell.attr["life"] = self.FIRE_LIFE
                elif cell.val == " " and cell.adjacent("A") > 0 and np.random.random() < self.GROWTH_CHANCE: #if adjacent to tree, chance to grow
                    cell.stage("A")
    
    def disp(self):
        for row in self.field:
            for cell in row:
                if str(cell) == "&":
                    self.stdscr.addstr(cell.y, cell.x, str(cell), curses.color_pair(1))
                else:
                    self.stdscr.addstr(cell.y, cell.x, str(cell))
        self.stdscr.refresh()
               
        # for row in self.field:
        #     for cell in row:
        #         stdscr.addstr(cell.y, cell.x, "({},{})".format(cell.x, cell.y))
        #         stdscr.refresh()

def main():
    try:
        f = Forest(blank = " ", speed = 1)
        f.simulate()
    except KeyboardInterrupt:
        f.destroy_curses()
    except BaseException as e:
        f.destroy_curses()
        print(traceback.format_exc())
if __name__ == '__main__':
    main()