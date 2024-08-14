import pygame
import numpy as np
from scipy.fft import fft
import sounddevice as sd
import time
from threading import Thread

class MusicPlayer:
    def __init__(self, volume, func_return):
        # init variables
        self.__exit, self.isPlaying = False, False
        self.repeat = True
        self.current_file_playing = ""
        self.__func_return = func_return
        self.current_song_lenght = 0

        self.volume = volume

        # init pygame
        pygame.mixer.init()

        # init threads
        self.__playerThread = Thread(target=self._playerT)


    def play(self, song_path):
        try:
            self.current_song_lenght = pygame.mixer.Sound(song_path).get_length()
        except FileNotFoundError:
            self.current_song_lenght = 0
            """ HERE HANDLE ERRORS AND RESET THE PLAYER IF THE SONG DOESNT PLAY"""
        self.isPlaying = True
        self.current_file_playing = song_path
        pygame.mixer.music.load(self.current_file_playing)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        try:
            self.__playerThread.start()
        except RuntimeError:
            pass

    def _playerT(self): # T for running as thread
        while True:
            while not self.__exit: 
                # EQUALIZER SHIT HERE BRO
                if self.isPlaying:
                    time.sleep(.1)

                elif pygame.mixer.music.get_pos == -1:
                    break
            
                else:
                    time.sleep(.1)
                self.__func_return(pygame.mixer.music.get_pos(), pygame.mixer.music.get_volume())

            if not self.repeat:
                pygame.mixer.music.stop()
                self.__exit = True
                break
            else:
                pygame.mixer.music.load(self.current_file_playing)
                pygame.mixer.music.play()
            

    def pause_unpause(self) -> None:
        if self.isPlaying:
            pygame.mixer.music.pause()
            self.isPlaying = False
        elif self.isPlaying == False:
            pygame.mixer.music.unpause()
            self.isPlaying = True


    def set_volume(self, volume) -> None:
        pygame.mixer.music.set_volume(volume)

    def lower_volume(self) -> None:
        if self.volume > 0:
            self.volume = round(self.volume - .1, 4)
            pygame.mixer.music.set_volume(self.volume)
    
    def higher_volume(self) -> None:
        if self.volume < 1:
            self.volume = round(self.volume + .1, 4)
            pygame.mixer.music.set_volume(self.volume)
    
    def get_full_lenght(self) -> int:
        return int(self.current_song_lenght)

    def stop(self) -> None:
       pygame.mixer.music.stop()
       self.__exit = True
       self.isPlaying = False
