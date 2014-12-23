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
    ""

def main():
    stdscr = initCurses()
    #stdscr.printw("hello world")  # no printw in python curses
    stdscr.addstr("hello world\n")
    stdscr.refresh()

    # start repl here
    keypress = stdscr.getch()

    curses.endwin()

main()
