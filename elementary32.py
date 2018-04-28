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
        self.FILL = "#"
        args = sys.argv[1:]
        
        keys = []
        for i in range(31, -1, -1):
            keys.append(format(i, "05b")) #  ['11111', '11110', '11101', '11100', ...]   len() = 32
        out = list(format(int(args[0]), "032b"))   #spits out ['1', '0', '0', ...]
        vals = [self.FILL if x == "1" else self.blank for x in out] #["#", " ", " ", ...]
        self.rules = dict(zip(keys,vals))  #{"111": " ", "110": "#", "101": " ", ...}

        
        if "--random" in args:
            for cell in self.field[0]:
                if np.random.random() < 0.2:
                    cell.stage(self.FILL)
        else:
            self.field[0,self.cols//2].stage(self.FILL)
        
        self.counter = 1    
        
    
    def tick(self):
        try:
            for cell in self.field[self.counter]:
                above = "".join(["1" if x == self.FILL else "0" for x in (cell.get_rel(-1, -2).val, cell.get_rel(-1, -1).val, cell.get_rel(-1, 0).val, cell.get_rel(-1, 1).val, cell.get_rel(-1, 2).val)]) #converts "# #" to "101". It's a mess but can't think of a better way
                cell.stage(self.rules[above])
            self.counter += 1
        except IndexError:
            pass
            
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