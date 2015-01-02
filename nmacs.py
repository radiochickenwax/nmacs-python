#!/usr/bin/python

import curses


class buffer:
    def initCurses():
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(1)    
        curses.use_default_colors()
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
                stdscr.addstr(lines[i])
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
                            #stdscr.move(cy-1,cx)
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
            
        
        def main(screen):
            stdscr = initCurses()
            lines = [ ]
            for i in range(0,100):
                lines.append(str(i) + " lots of lines\n")

            scrollBufferREPL(lines,stdscr)
            # curses.endwin() # not needed since curses.wrapper() handles this

buffer.main()
#curses.wrapper(buffer.main)
