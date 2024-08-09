import curses
from curses import wrapper
from time import sleep, monotonic
from threading import Thread


class navigator:
    def __init__(self, min_y, min_x):
        self._min_x = min_x
        self._min_y = min_y


    def _drawBox(self, stdscr, y, x, h, w):
        #result =  + "┐\n" ++ "└" + "─" * (w - 2) + "┘"
        
         # LOCAL COORDS OF THE BOX
        X = x + w
        Y = y + h

        stdscr.addstr(y, x, "┌" + "─" * (w - 2) + "┐")
        for n in range(h - 2):
            stdscr.addstr(n + 1, x, "│" + " " * (w - 2) + "│")
        stdscr.addstr(Y, x, "└" + "─" * (w - 2) + "┘")

        
       
        # editing the box
        #stdscr.addstr(y, x, result)

    def printSubWin(self, stdscr, y, x, h, w):
        self._drawBox(stdscr, y, x, h, w)



class equalizer:
    def __init__(self, min_y, min_x):
        self._min_x = min_x
        self._min_y = min_y
        
    def _drawBox(self, stdscr, y, x, h, w):
        result = "┌" + "─" * w + "┐\n" + ("│" + " " * w + "│\n") * h + "└" + "─" * w + "┘"  
        # LOCAL COORDS OF THE BOX
        X = x + w
        Y = y + h 
        
        # here we edit the box
        stdscr.addstr(y, x, result)
        for n in range(10): # APPENDING THE STRING THIS WAY BECAUSE IT WILL BE USEFUL WHEN ADDING THE EQUALIZER
            pos_x, pos_y = int((X // 2) - ((n + 1))), int(Y  // 2)

            stdscr.addstr(pos_y, pos_x, "AA")
        

    def printSubWin(self, stdscr, y, x, h, w):
        self._drawBox(stdscr, y, x, h, w)

class MainWindow:
    def __init__(self, fps=30) -> None:
        self.fps = fps
        self.__on = True

        #initializing the sub-windows
        self.__eq = equalizer(0, 0)
        self.__nv = navigator(0, 0)

        self._wrapperThread = Thread(target=self._wrapper)
   
    def __exit__(self):
        self.__on = False


    def _wrapper(self):
        wrapper(self._updateWindow)

    def _updateWindow(self, stdscr):
        stdscr.clear()

        while self.__on:
            self._editScreen(stdscr)
            stdscr.refresh()
            sleep(1 / self.fps)

    
    # This function takes care of everything that will be seen on the frame.
    def _editScreen(self, s):
        sY, sX = s.getmaxyx() # screen X lenght and screen Y lenght
        self.__eq.printSubWin(s, 0, 0, int(sY/ 1.5), int(sX / 1.5))
        self.__nv.printSubWin(s, 0, int(sX / 1.5) + 2, int(sY / 1.5), sX - int(sX/1.5) - 2)
        #s.addstr(16, 16, str(s.getmaxyx()))



    def start(self):
        self._wrapperThread.start()

    def stop(self):
        self.__exit__()

window = MainWindow(fps=10)
window.start()
sleep(10)
window.stop()
