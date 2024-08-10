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

        self.current_index = 0
        self.current_path = "E:/d/ultraviolet/"


    def _drawBox(self, stdscr, y, x, h, w):
         # LOCAL COORDS OF THE BOX
        X = x + w
        Y = y + h

        # KEEPS TRACK OF KEYS

        # DRAWING THE BOX FIRST
        stdscr.addstr(y, x, "┌" + "─" * (w - 2) + "┐")
        for n in range(h - 2):
            stdscr.addstr(y + n + 1, x, "│" + " " * (w - 2) + "│")
        stdscr.addstr(Y - 1, x, "└" + "─" * (w - 2) + "┘")

        #grabbing files and folders from the given directory
        temp_val = h - self.current_index
        path = list(pathlib.Path(self.current_path).iterdir())[self.current_index :h + self.current_index - 2]


        files = [p for p in path if p.is_file()]
        folders = [p for p in path if p.is_dir()]
        files.sort()
        folders.sort()

        n = 0
        for f in folders:
            stdscr.addstr(y + n + 1, x + 1, f.name[:w - 2])
            n += 1
        for f in files:
            stdscr.addstr(y + n + 1, x + 1, f.name[:w - 2])
            n += 1
        



       
        # editing the box
        #stdscr.addstr(y, x, result)

    def printSubWin(self, stdscr, y, x, h, w):
        self._drawBox(stdscr, y, x, h, w)


        
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
        self.fps = fps
        self.__on = True

        self.__stdscr = None

        #initializing the sub-windows
        self.__eq = equalizer(0, 0, (True, True))
        self.__nv = navigator(0, 0, (True, True))
        self.__mp = musicplayer(0, 0, (False, True))

        self.__wrapperThread = Thread(target=self._wrapper)
        self.__grabKeyThread = Thread(target=self._grabKey)
   
    def __exit__(self):
        
        self.__on = False


    def _wrapper(self):
        wrapper(self._updateWindow)

    def _updateWindow(self, stdscr):
        self.__stdscr = stdscr
        stdscr.clear()

        while self.__on:
            self._editScreen(stdscr)
            stdscr.refresh()
            sleep(1 / self.fps)
    
    def _grabKey(self):
        text = "None"
        while self.__stdscr != None and self.__on:
            key = self.__stdscr.getch()

            windowUsed = self.__nv

            if key == 27: # ESCAPE PRESSED
                self.stop()
                break

            # FOR NAVIGATION
            if key == curses.KEY_UP:
                self.
            elif key == curses.KEY_DOWN:
                text = "DOWN"
            
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
        self.__nv.printSubWin(s, 0, int(sX / 1.5) + 2, sY, sX - int(sX/1.5) - 2)
        self.__mp.printSubWin(s, sY - 3, 1, 3, int(sX / 1.5))
        #s.addstr(16, 16, str(s.getmaxyx()))



    def start(self):
        self.__wrapperThread.start()
        self.__grabKeyThread.start()

    def stop(self):
        self.__exit__()


window = MainWindow(fps=10)
window.start()
