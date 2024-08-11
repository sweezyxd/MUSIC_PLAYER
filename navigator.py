import curses
from curses import wrapper
from time import sleep, monotonic
from threading import Thread
import pathlib


class musicplayer:
    def __init__(self, min_y, min_x, isStatic):
        self.__isStatic = isStatic
        self.__min_x = min_x
        self.__min_y = min_y

    def _drawBox(self, stdscr, y, x, h, w):
        # LOCAL COORDS OF THE BOX
        X = x + w
        Y = y + h

        stdscr.addstr(y, x, "┌" + "─" * (w - 2) + "┐")
        for n in range(h - 2):
            stdscr.addstr(y + n + 1, x, "│" + " " * (w - 2) + "│")
        stdscr.addstr(Y - 1, x, "└" + "─" * (w - 2) + "┘")


    def printSubWin(self, stdscr, y, x, h, w):
        self._drawBox(stdscr, y, x, h, w)



class navigator:
    def __init__(self, min_y, min_x, isStatic):
        self.__isStatic = isStatic
        self.__min_x = min_x
        self.__min_y = min_y
        self.h = 0

        # For navigating through folders
        self.filesNumber = 0
        self.current_fileIndex = 0 # the index of the item that shows the first in the list.
        self.current_index = 0 # the index of where the cursor is.
        self.current_path = "/etc"
        self.current_fileSelected = None

    def _getFilesFromPath(self, path) -> list:
        #grabbing files and folders from the given directory.
        try:

            path = list(pathlib.Path(self.current_path).iterdir())
        except FileNotFoundError:
            self.current_path = "/"
            path = list(pathlib.Path(self.current_path).iterdir())
        
        files = [[p, curses.color_pair(0)] for p in path if p.is_file()]
        folders = [[p, curses.color_pair(1)] for p in path if p.is_dir()]

        files.sort()
        folders.sort()
        
        self.filesNumber = len(folders + files)

        items = (folders + files)

        return items


    def _drawBox(self, stdscr, y, x, h, w):
        self.h = h
         # LOCAL COORDS OF THE BOX
        X = x + w
        Y = y + h

        # KEEPS TRACK OF KEYS

        # DRAWING THE BOX FIRST
        stdscr.addstr(y, x, "┌" + "─" * (w - 2) + "┐")
        for n in range(h - 2):
            stdscr.addstr(y + n + 1, x, "│" + " " * (w - 2) + "│")
        stdscr.addstr(Y - 1, x, "└" + "─" * (w - 2) + "┘")
        

        # This lists all the items in the parent folder
        self.items = [["..", curses.color_pair(1)]] + [[i[0].name[:w - 2], i[1]] for i in self._getFilesFromPath(self.current_path)]
        self.items = self.items[self.current_fileIndex: h + self.current_fileIndex - 2] # this takes only the ones that should be shown

        for i, f in enumerate(self.items):
            stdscr.addstr(y + i + 1, x + 1, f + " " * (w - 2 - len(f)), curses.A_REVERSE if i == self.current_index else 0)
            if i == self.current_index:
                stdscr.addstr(y + i + 1, x + 1, f + " " * (w - 2 - len(f)), curses.A_REVERSE)
                self.current_fileSelected = f
            else:
                stdscr.addstr(y + i + 1, x + 1, f + " " * (w - 2 - len(f)))
        

    # FOR USER
    #
    #

    def printSubWin(self, stdscr, y, x, h, w):
        self._drawBox(stdscr, y, x, h, w)

    def up(self):
        if self.current_index > 0:
            self.current_index -= 1
        elif self.current_index <= 0 and self.current_fileIndex > 0:
            self.current_fileIndex -= 1

    def down(self):
        if self.current_index < self.h - 3:
            self.current_index += 1
        elif self.current_index <= self.h - 3 and self.current_fileIndex < self.filesNumber - self.h + 2:
            self.current_fileIndex += 1

    def enter(self):
        if self.current_fileSelected == "..":
            self.current_path = str(pathlib.Path(self.current_path).parent)


        
class equalizer:
    def __init__(self, min_y, min_x, isStatic):

        self.__isStatic = isStatic
        self.__min_x = min_x
        self.__min_y = min_y
        
    def _drawBox(self, stdscr, y, x, h, w):
         # LOCAL COORDS OF THE BOX
        X = x + w
        Y = y + h

        stdscr.addstr(y, x, "┌" + "─" * (w - 2) + "┐")
        for n in range(h - 2):
            stdscr.addstr(y + n + 1, x, "│" + " " * (w - 2) + "│")
        stdscr.addstr(Y - 1, x, "└" + "─" * (w - 2) + "┘")
        

    def printSubWin(self, stdscr, y, x, h, w):
        self._drawBox(stdscr, y, x, h, w)

class MainWindow:
    def __init__(self, fps=30) -> None:
        # DEFINING COLORS.
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)


        self.fps = fps
        self.__on = True

        self.__stdscr = None

        #initializing the sub-windows
        self.__eq = equalizer(0, 0, (True, True))
        self.__nv = navigator(0, 0, (True, True))
        self.__mp = musicplayer(0, 0, (False, True))

        self.__wrapperThread = Thread(target=self._wrapper)
   
    def __exit__(self):
        self.__on = False


    def _wrapper(self):
        wrapper(self._updateWindow)


    def _updateWindow(self, stdscr):
        self.__stdscr = stdscr
        self.__stdscr.nodelay(True)
        curses.curs_set(0)
        stdscr.clear()

        while self.__on:
            self._grabKey()
            self._editScreen(stdscr)
            stdscr.refresh()


    def _grabKey(self):
        key = self.__stdscr.getch()

        #windowUsed = self.__nv

        if key == 27: # ESCAPE PRESSED
            self.stop()
            

        # FOR NAVIGATION
        if key == curses.KEY_UP:
            self.__nv.up()
        elif key == curses.KEY_DOWN:
            self.__nv.down()
        elif key == 10: # ENTER
            self.__nv.enter()
        
        # FOR PLAYING/PAUSING ETC
        elif key == curses.KEY_LEFT: # go backwards
            pass
        elif key == curses.KEY_RIGHT: # go forward
            pass 

    
    # This function takes care of everything that will be seen on the frame.
    def _editScreen(self, s):
        sY, sX = s.getmaxyx() # screen X lenght and screen Y lenght
        sX -= 1 # MAX USABLE X

        """
        REMINDER: ARGS TAKE (Y, X, H, W) AND NOT (Y1, X1, Y2, X2)
        """

        self.__eq.printSubWin(s, 0, 1, sY - 3, int(sX / 1.5))
        self.__mp.printSubWin(s, sY - 3, 1, 3, int(sX / 1.5))
        self.__nv.printSubWin(s, 0, int(sX / 1.5) + 1, sY, sX - int(sX/1.5) - 1)


    def start(self):
        self.__wrapperThread.start()

    def stop(self):
        self.__exit__()


window = MainWindow(fps=10)
window.start()
