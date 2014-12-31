#!/usr/bin/python

import curses

def initCurses():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)    
    return stdscr

def getStartLine(lines,stdscr,currentLine):
    cy,cx = stdscr.getyx()
    minBoundary = currentLine - cy
    if (minBoundary >= 0):
        returnVal = minBoundary
    else:
        returnVal =  0
    return returnVal

def getFinishLine(lines,stdscr,currentLine):
    cy,cx = stdscr.getyx()
    ymax,xmax = stdscr.getmaxyx()
    maxBoundary = currentLine + ymax - cy -1
    if (maxBoundary < len(lines)):
        returnVal = maxBoundary
    else:
        returnVal = len(lines)
    return returnVal

def displayLines(lines,stdscr,startLine,finishLine):
    ty,tx = stdscr.getyx()
    stdscr.move(0,0)
    stdscr.clear()
    for i in range(startLine,finishLine):
        stdscr.addstr(i,0,lines[i])
        #stdscr.addstr(startLine-i,0,lines[i])
        #         cy,cx=stdscr.getyx()
        #         stdscr.move(cy+1,0)
    stdscr.move(ty,tx)
    stdscr.refresh()

def scrollBufferREPL(lines,stdscr):
    startLine = 0
    currentLine = 0
    ymax,xmax = stdscr.getmaxyx()
    finishLine = ymax-1
    displayLines(lines,stdscr,startLine,finishLine)
    stdscr.move(0,0)
    editorRunning = True
    while (editorRunning):
        ymax,xmax = stdscr.getmaxyx()
        cy,cx = stdscr.getyx()
        key = stdscr.getch()
        # handle key presses
        if (key == curses.KEY_UP): 
            if (cy-1 >= 0): # don't scroll
                stdscr.move(cy-1,0)
                currentLine -= 1
            else: # scroll display
                if (currentLine-1 >= 0):
                    stdscr.move(cy-1,cx)
                    currentLine -= 1
                    startLine -= 1
                    finishLine -= 1
                
        elif (key == curses.KEY_DOWN):
            #stdscr.move(cy+1,0)
            if (cy+1 < ymax-1): # don't scroll
                if (cy+1 < len(lines)):
                    stdscr.move(cy+1,cx)
                    currentLine = currentLine +1
            else: # scroll display
                if (currentLine+1 < len(lines)):
                    currentLine += 1
                    # startLine = getStartLine(lines,stdscr,currentLine)
                    # finishLine = getFinishLine(lines,stdscr,currentLine)
                    startLine += 1
                    finishLine += 1
        else: # default keypress
            print ""
        # finished conditionals, display lines
        displayLines(lines,stdscr,startLine,finishLine)
            
        
def main():
    stdscr = initCurses()
    lines = [ ]
    #stdscr.printw("hello world")  # no printw in python curses
    for i in range(0,99):
        #stdscr.addstr(i + "lots of lines")
        lines.append(str(i) + " lots of lines")
    #ymax,xmax = stdscr.getmaxyx()
    #displayLines(lines,stdscr,0,ymax-1)
    #stdscr.move(10,10)
    #stdscr.refresh()

    # start repl here
    #keypress = stdscr.getch()
    scrollBufferREPL(lines,stdscr)
    

    curses.endwin()

main()
