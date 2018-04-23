#!/usr/bin/env python3
import time
import numpy as np
import curses
import sys
import traceback

class CellAut(object):
    def __init__(self, blank = " ", speed = 1.0):
        self.stdscr = curses.initscr()
        self.rows, self.cols = self.stdscr.getmaxyx()
        self.rows -= 1 #for some reason I cant use curses to print in the bottom right corner so i gotta delete a row
        self.blank = blank
        self.speed = speed
        self.field = np.empty((self.rows, self.cols), object)
        for y in range(self.rows):
            for x in range(self.cols):
                self.field[y,x] = CellAut.Cell(self, x, y, self.blank)


        # if self.cols > maxX or self.rows > maxY - 1: 
        #     self.destroy_curses()
        #     raise RuntimeError("Automaton field exceeds terminal size")
        curses.noecho()
        curses.start_color()
        curses.curs_set(False)
        curses.use_default_colors()
        # self.stdscr.addstr(57,202,"A")
        # self.stdscr.addstr(56,203,"A")
        # self.stdscr.addstr(57,203,"A")
        # self.stdscr.refresh()
        # time.sleep(3)
        # raise Exception

                
    def firstframe(self):
        #Generate start field, init additional variables, override to change start state
        #self.i = 0
        for row in self.field:
            for cell in row:
                if np.random.random() < 0.2:
                    cell.stage("1")
        
    def simulate(self):
        starttime = time.time()
        self.firstframe()
        self.commit()
        while True:
            self.disp()    #show everything
            self.tick()    #process each cell
            self.commit()  #copy staged value to actual value
            time.sleep(self.speed - ((time.time() - starttime) % self.speed)) #sleep an accurate amount of time, accounting for time to process

    
    def tick(self):
        for row in self.field:
            for cell in row:
                cell.stage(str(int(str(cell)) + 1))
    
    def commit(self):
        for row in self.field:
            for cell in row:
                cell.commit()
    
    def disp(self):
        #TODO use ncurses
        for row in self.field:
            for cell in row:
                self.stdscr.addstr(cell.y, cell.x, str(cell))
        self.stdscr.refresh()
    
    def destroy_curses(self):
        curses.echo()
        curses.endwin()
        curses.curs_set(True)
    
    class Cell(object):
        def __init__(self, parent, x, y, val, attr = {}):
            self.parent = parent
            self.x = x
            self.y = y
            self.val = val
            self.staged = val
            self.attr = attr
            
        def __str__(self):
            return self.val

        def adjacent(self, search):
            count = 0
            for i in [(self.y-1, self.x), (self.y+1, self.x), (self.y, self.x-1), (self.y, self.x+1)]: #y always comes first! dont forget!!
                if -1 in i:
                    continue #skip -1 because python will wrap it around
                try:
                    v = str(self.parent.field[i])
                except IndexError:
                    continue
                if v == search:
                    count += 1
            return count

        def surrounding(self, search): #like adjacent but with diagonals
            count = 0
            for i in [(self.y-1, self.x), (self.y+1, self.x), (self.y, self.x-1), (self.y, self.x+1), (self.y-1, self.x-1), (self.y+1, self.x+1), (self.y-1, self.x+1), (self.y+1, self.x-1)]: 
                if -1 in i:
                    continue #skip -1 because python will wrap it around
                try:
                    v = str(self.parent.field[i])
                except IndexError:
                    continue
                if v == search:
                    count += 1
            return count

        def stage(self, v):
            self.staged = v
        
        def commit(self):
            self.val = self.staged

if __name__ == '__main__':
    try:
        test = CellAut(blank = "0")
        test.simulate()
    except KeyboardInterrupt:
        curses.echo()
        curses.endwin()
        curses.curs_set(True)
    except BaseException as e:
        curses.echo()
        curses.endwin()
        curses.curs_set(True)
        print(traceback.format_exc())