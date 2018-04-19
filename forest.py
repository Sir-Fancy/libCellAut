#!/usr/bin/env python3
from libCellAut import CellAut
import numpy as np

class Forest(CellAut):
    def firstframe(self):
        #Generate start field, init additional variables, override to change start state

        for row in self.field:
            for cell in row:
                if np.random.random() < 0.01:
                    cell.stage("#")
    
    def tick(self):
        #self.stage[:] = self.field[:]
        for row in self.field:
            for cell in row:
                if cell.val == " " and cell.adjacent("#") > 0:
                    cell.stage("#")

def main():
    f = Forest(blank = " ", speed = 0.5)
    f.simulate()


if __name__ == '__main__':
    main()