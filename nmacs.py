#!/usr/bin/python

import curses
import os

class buffer:
    def __init__(self):
        #self.stdscr = self.initCurses()
        self.stdscr = curses.initscr()
        curses.use_default_colors()
        self.lines = []
        self.mode = "text"
        self.cy = 0
        self.cx = 0
        self.ymax, self.xmax = self.stdscr.getmaxyx()

        self.currentLine = 0

        self.ystartLine = 0
        self.yfinishLine = self.ymax-1

        self.currentCol = 0
        self.xstartCol = 0
        self.xfinishCol = self.xmax-1

        for i in range(0,100):
            self.lines.append(str(i) + " lots of lines\n")
        self.scrollBufferREPL()

    def initCurses(self):
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(1)    
        curses.use_default_colors()
        return stdscr
    
    def openFile(self):
        del self.lines[:] # clear lines
        self.currentLine=0
        self.ymax,self.xmax = self.stdscr.getmaxyx()
        self.ystartLine=0
        self.yfinishLine=self.ymax-1
        self.stdscr.move(0,0)
        with open('./nmacs.py') as f:
            for line in f:
                self.lines.append(line)
                

    def getStartLine(self):
        self.cy,self.cx = self.stdscr.getyx()
        minBoundary = self.currentLine - self.cy
        if (minBoundary >= 0):
            returnVal = minBoundary
        else:
            returnVal =  0
        return returnVal

    def getFinishLine(self):
        self.cy,self.cx = self.stdscr.getyx()
        self.ymax,self.xmax = self.stdscr.getmaxyx()
        maxBoundary = self.currentLine + self.ymax - self.cy -1
        if (maxBoundary < len(self.lines)):
            returnVal = maxBoundary
        else:
            returnVal = len(lines)
        return returnVal
            
    def displayLines(self):
        ty,tx = self.stdscr.getyx()
        self.stdscr.move(0,0)
        self.stdscr.clear()
        for i in range(self.ystartLine,self.yfinishLine):
            line = self.lines[i]
            for j in range(self.xstartCol,min(len(line), self.xfinishCol)):
                self.stdscr.addch(line[j])
        self.stdscr.move(ty,tx)
        self.stdscr.refresh()
    
    def stats(self):
        lineNumber = self.currentLine + 1
        ty,tx = self.stdscr.getyx()
        self.cy,self.cx = ty,tx
        self.ymax,self.xmax =  self.stdscr.getmaxyx()
        self.stdscr.move(self.ymax-1,0)
        self.stdscr.clrtoeol()
        self.stdscr.attron(curses.A_BOLD)
        self.stdscr.attron(curses.A_REVERSE)
        statString = "cx:" + str(self.cx )
        statString += ",cy:" + str(self.cy)
        statString += ",cl:" + str(self.currentLine)
        statString += ",sl:" + str(self.ystartLine)
        statString += ",fl:" + str(self.yfinishLine)
        statString += ",lines:" + str(len(self.lines))
        statString += ",ll:" + str(len(self.lines[self.currentLine]))
        statString += ",cc:" + str(self.currentCol)
        statString += ",sx:" + str(self.xstartCol)
        statString += ",fx:" + str(self.xfinishCol)
        statString += ",cols:" + str(self.yfinishLine)
        self.stdscr.addstr(statString)
        self.stdscr.attroff(curses.A_BOLD)
        self.stdscr.attroff(curses.A_REVERSE)
        self.stdscr.move(ty,tx)

    def scrollBufferREPL(self):
        self.displayLines()
        self.stdscr.move(0,0)
        self.editorRunning = True

        while (self.editorRunning):

            self.ymax,self.xmax = self.stdscr.getmaxyx()
            self.cy,self.cx = self.stdscr.getyx()
            key = self.stdscr.getch()
            # handle key presses

            if (key == curses.KEY_UP): 
                if (self.cy-1 >= 0): # don't scroll
                    self.stdscr.move(self.cy-1,self.cx)
                    self.currentLine -= 1
                else: # scroll display
                    if (self.currentLine-1 >= 0):
                        #stdscr.move(cy-1,cx)
                        self.currentLine -= 1
                        self.ystartLine -= 1
                        self.yfinishLine -= 1
                
            elif (key == curses.KEY_DOWN):
                #stdscr.move(cy+1,0)
                if (self.cy+1 < self.ymax-1): # don't y-scroll down
                    if (self.cy+1 < len(self.lines)):
                        if (self.currentCol <
                            len(self.lines[self.currentLine+1])):
                            self.stdscr.move(self.cy+1,self.cx)
                            self.currentLine += 1
                else: # y-scroll down
                    if (self.currentLine+1 < len(self.lines)):
                        self.currentLine += 1
                        # ystartLine = getStartLine(lines,stdscr,currentLine)
                        # yfinishLine = getFinishLine(lines,stdscr,currentLine)
                        self.ystartLine += 1
                        self.yfinishLine += 1

            elif (key == 15): # ctrl-o: open file
                    self.openFile()

            elif (key == curses.KEY_RIGHT):
                if (len(self.lines[self.currentLine]) < self.xmax): # don't consider scrolling 
                    if (self.cx+1 < len(self.lines[self.currentLine])):
                        self.stdscr.move(self.cy,self.cx+1)
                        self.currentCol += 1
                else: # consider scroll x direction
                    if (self.cx+1 < self.xmax):
                        self.stdscr.move(self.cy,self.cx+1)
                    else:
                        if (self.cx+1 <= len(self.lines[self.currentLine])):
                            self.currentCol += 1
                            self.xstartCol += 1
                            self.xfinishCol += 1

            elif (key == curses.KEY_LEFT):                
                
                if(self.cx-1 >= 0): # don't scroll
                    self.stdscr.move(self.cy,self.cx-1)
                    self.currentCol -= 1
                else: # consider scrolling
                    if (self.xstartCol-1 >= 0):
                        self.currentCol -= 1
                        self.xstartCol -= 1
                        self.xfinishCol -= 1
                        

            elif (key == curses.KEY_BACKSPACE):
                before = self.lines[self.currentLine][:self.cx-1]
                after = self.lines[self.currentLine][self.cx:]
                self.lines[self.currentLine] = before + after
                # note the following doesn't check window x-length.
                # which really means gotta implement horiz scrolling
                self.stdscr.move(self.cy,self.cx-1)
                self.currentCol -= 1

            elif (key == 10 ): #curses.KEY_ENTER):
                before = self.lines[self.currentLine][:self.cx-1]
                after = self.lines[self.currentLine][self.cx:]
                before += '\n'
                

            else: # default keypress (lineGap)
                if (self.cx+1 < self.xmax):
                    before = self.lines[self.currentLine][:self.cx] + chr(key)
                    after = self.lines[self.currentLine][self.cx:]
                    self.lines[self.currentLine] = before + after
                    # note the following doesn't check window x-length.
                    # which really means gotta implement horiz scrolling
                    self.stdscr.move(self.cy,self.cx+1)
                    self.currentCol += 1

            # finished conditionals, display lines
            self.displayLines()
            self.stats()
            
        
def main(screen):
    this_buffer = buffer()

#     curses.endwin()

if __name__ == '__main__':
    curses.wrapper(main)
