#!/usr/bin/python

import curses

def initCurses():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    return stdscr

def getStartLine():
    "" 

def getFinishLine():
    ""
def displayLines(lines,stdscr,startLine,finishLine):
    stdscr.move(0,0)
    for i in range(startLine,finishLine):
        stdscr.addstr(i,0,lines[i])
#         cy,cx=stdscr.getyx()
#         stdscr.move(cy+1,0)
    stdscr.move(0,0)

def main():
    stdscr = initCurses()
    lines = [ ]
    #stdscr.printw("hello world")  # no printw in python curses
    for i in range(0,99):
        #stdscr.addstr(i + "lots of lines")
        lines.append(str(i) + "lots of lines")
    ymax,xmax = stdscr.getmaxyx()
    displayLines(lines,stdscr,0,ymax-1)
    #stdscr.move(10,10)
    stdscr.refresh()



    # start repl here
    keypress = stdscr.getch()

    curses.endwin()

main()
