import player
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

        self.player = player.MusicPlayer(1, self.grabSongInfo)

        self.stdscr = None

        """  ↻ ◁ || ⏸ ▶ ↺  """

        self.time = 0
        self.song_name = ""


    def _timeToStr(self, time) -> str:
        minutes = (time // 1000) // 60
        seconds = (time // 1000) - minutes * 60
        if minutes < 0:
            return "00:00"
        minutes = str(minutes)
        seconds = str(seconds)
        return "0" * (2 - len(minutes)) + minutes + ":" + (2 - len(seconds)) * "0" + seconds 

    def _drawOtherThings(self, y, x, h, w):
        slot_area = 30
        time_area = 6
        # TimeStamp
        self.stdscr.addstr(y + 1, x + 4, "─" * (w - 6))
        

        self.stdscr.addstr(y + 1, x + 2, "▶" if self.player.isPlaying == False else "⏸")

        # printing the song player information
        self.stdscr.addstr(y, x + 2, " Playing: "  + self.song_name[:slot_area] + ". ")

        time = self._timeToStr(self.time)
        full_time = self._timeToStr(self.player.get_full_lenght())
        self.stdscr.addstr(y, x + w - 20, " " + time + " / " + full_time + " ")
        self.stdscr.addstr(y, x + w - 50, " Volume: " + str(int(self.player.volume * 100)) + "% ")

    def _drawBox(self, stdscr, y, x, h, w):
        self.stdscr = stdscr
        # LOCAL COORDS OF THE BOX
        X = x + w
        Y = y + h

        # Drawing the box
        self.stdscr.addstr(y, x, "┌" + "─" * (w - 2) + "┐")
        for n in range(h - 2):
            self.stdscr.addstr(y + n + 1, x, "│" + " " * (w - 2) + "│")
        self.stdscr.addstr(Y - 1, x, "└" + "─" * (w - 2) + "┘")


        # Drawing Other things
        self._drawOtherThings(y, x, h, w)

    def printSubWin(self, stdscr, y, x, h, w):
        self._drawBox(stdscr, y, x, h, w)

    def grabSongInfo(self, time, volume):
        self.time = time
        self.volume = volume * 100

    def play(self, name):
        self.player.play(name)



class navigator:
    def __init__(self, min_y, min_x, isStatic):
        self.__isStatic = isStatic
        self.__min_x = min_x
        self.__min_y = min_y
        self.h = 0

        # For navigating through folders
        self.filesNumber = 0
        self.current_file_playing = ""
        self.current_fileIndex = 0 # the index of the item that shows the first in the list.
        self.current_index = 0 # the index of where the cursor is.
        self.current_path = ""
        self.current_fileSelected = None

    def _getFilesFromPath(self, path) -> list:
        #grabbing files and folders from the given directory.
        try:

            path = list(pathlib.Path(self.current_path).iterdir())
        except FileNotFoundError:
            self.current_path = ""
            path = list(pathlib.Path(self.current_path).iterdir())
        
        files = [[p, curses.color_pair(0)] for p in path if (p.is_file() and (p.name[-3:] == "wav" or p.name[-3:] == "mp3"))]
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
        self.items = [["..", curses.color_pair(2)]] + [[i[0].name, i[1]] for i in self._getFilesFromPath(self.current_path)]
        self.items = self.items[self.current_fileIndex: h + self.current_fileIndex - 2] # this takes only the ones that should be shown

        for i, f in enumerate(self.items):
            text = f[0]
            if str(pathlib.Path(self.current_path) / f[0]) == self.current_file_playing:
                text = "▷ " + text
            if i == self.current_index:
                stdscr.addstr(y + i + 1, x + 1, text[:w - 2] + " " * (w - 2 - len(f[0])), curses.A_REVERSE)
                self.current_fileSelected = f
            else:
                stdscr.addstr(y + i + 1, x + 1, text[:w - 2] + " " * (w - 2 - len(f[0])), f[1])
        
        #stdscr.addstr(10, 10, str(pathlib.Path(self.current_path) / self.current_fileSelected[0]))

    # FOR USER
    #
    #

    def resetValues(self):
        self.filesNumber = 0
        self.current_fileIndex = 0 # the index of the item that shows the first in the list.
        self.current_index = 0 # the index of where the cursor is.
        self.current_fileSelected = None

    def printSubWin(self, stdscr, y, x, h, w, current_file_playing):
        self.current_file_playing = current_file_playing
        self._drawBox(stdscr, y, x, h, w)

    def up(self):
        if self.current_index > 0:
            self.current_index -= 1
        elif self.current_index <= 0 and self.current_fileIndex > 0:
            self.current_fileIndex -= 1

    def down(self):
        if self.current_index < self.h - 3 and self.current_index < self.filesNumber:
            self.current_index += 1
        elif self.current_index <= self.h - 3 and self.current_fileIndex < self.filesNumber - self.h + 3:
            self.current_fileIndex += 1

    def enter(self) -> list[str]:
        if self.current_fileSelected[0] == "..":
            self.current_path = str(pathlib.Path(self.current_path).resolve().parent)
            self.resetValues()
        
        elif self.current_fileSelected[1] == curses.color_pair(1):
            self.current_path = str(pathlib.Path(self.current_path) / self.current_fileSelected[0])
            self.resetValues()

        elif self.current_fileSelected[1] == curses.color_pair(0):
            songs = []
            for f in self.items:
                if f[1] == curses.color_pair(0): # curses.pair_color(0) indicates that the item is a file and not a folder
                    songs.append(str(pathlib.Path(self.current_path) / f[0]))
            song_index = songs.index(str(pathlib.Path(self.current_path) / self.current_fileSelected[0]))
            return songs[song_index:] + songs[:song_index]

        return None
    
        
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
        # Start curses mode
        #curses.initscr()
        
        # Enable color mode

        self.fps = fps
        self.__on = True

        self.__stdscr = None

        #initializing the sub-windows
        self.__eq = equalizer(0, 0, (True, True))
        self.__mp = musicplayer(0, 0, (False, True))
        self.__nv = navigator(0, 0, (True, True))

        self.__wrapperThread = Thread(target=self._wrapper)
   
    def __exit__(self):
        self.__on = False


    def _wrapper(self):
        wrapper(self._updateWindow)


    def _updateWindow(self, stdscr):
        self.__stdscr = stdscr
        self.__stdscr.nodelay(True)
        stdscr.clear()

        # Enabling color mode and defining color pairs
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_YELLOW)

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
            song_list = self.__nv.enter()
            if song_list != None:
                self.__mp.play(song_list)

        elif key == ord(" "):
                self.__mp.player.pause_unpause()

        elif key == ord("=") or key == ord("+"):
            self.__mp.player.higher_volume()
        elif key == ord("-"):
            self.__mp.player.lower_volume()
        
        
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
        self.__nv.printSubWin(s, 0, int(sX / 1.5) + 1, sY, sX - int(sX/1.5) - 1, self.__mp.player.current_file_playing)


    def start(self):
        self.__wrapperThread.start()

    def stop(self):
        self.__exit__()


window = MainWindow(fps=10)
window.start()
