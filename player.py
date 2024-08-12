import pygame
import numpy as np
from scipy.fft import fft
import sounddevice as sd
import time
from threading import Thread

class MusicPlayer:
    def __init__(self, func_return):
        # init variables
        self.__exit, self.__isPlaying = False, False
        self.current_file_playing = ""
        self.__func_return = func_return

        # init pygame
        pygame.mixer.init()

        # init threads
        self.__playerThread = Thread(target=self._playerT)


    def play(self, song_path):
        self.__isPlaying = True
        self.current_file_playing = song_path
        pygame.mixer.music.load(self.current_file_playing)
        pygame.mixer.music.play()
        self.__playerThread.start()

    def _playerT(self): # T for running as thread
        while True:
            while not self.__exit:
                # EQUALIZER SHIT HERE BRO
                if self.__isPlaying:
                    time.sleep(1)
                else:
                    pass
                self.__func_return(pygame.mixer.music.get_pos(), pygame.mixer.music.get_volume())
            if not self.repeat:
                pygame.mixer.music.stop()
                break
            else:
                pygame.mixer.music.rewind()
            

    def pause_unpause(self):
        if self.__isPlaying:
            pygame.mixer.music.pause()
            self.__isPlaying = False
        elif self.__isPlaying == False:
            pygame.mixer.music.unpause()
            self.__isPlaying = True


    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def stop(self):
       pygame.mixer.music.stop()
       self.__exit = True
       self.__isPlaying = False
