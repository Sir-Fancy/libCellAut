#!/usr/bin/env python3
from libCellAut import CellAut
import numpy as np

class Forest(CellAut):
    def firstframe(self):
        #Generate start field, init additional variables, override to change start state
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
                elif cell.val == "A" and np.random.random() < 0.01:
                    cell.stage("&")
                    cell.attr["life"] = 3

def main():
    f = Forest(rows = 20, cols = 70, blank = " ", speed = 0.5)
    f.simulate()


if __name__ == '__main__':
    main()