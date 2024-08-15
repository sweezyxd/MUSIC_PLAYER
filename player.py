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
        self.repeat = 2
        self.current_file_playing = ""
        self.songs_list = []
        self.__func_return = func_return
        self.current_song_length = 0
        self.index = 0

        self.volume = volume

        # init pygame
        pygame.mixer.init()

        # init threads
        self.__playerThread = Thread(target=self._playerT)


    def play(self, songs_paths):
        try:
            self.isPlaying, self.__exit = False, True
            while True:
                if not self.__playerThread.is_alive():
                    self.songs_list = songs_paths
                    self.current_file_playing = self.songs_list[0]
                    self.index = 0
                    self.__playerThread = Thread(target=self._playerT)
                    self.__playerThread.start()
                    break
            

        except FileNotFoundError:
            self.current_song_length = 0


    def _playSong(self):
        pygame.mixer.music.load(self.current_file_playing)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        self.current_song_length = pygame.mixer.Sound(self.current_file_playing).get_length() * 1000
        self.isPlaying, self.__exit = True, False
        
            
    def _playerT(self): # T for running as thread
        self._playSong()
        self.index = 1
        while not self.__exit:
            while not self.__exit: 
                # EQUALIZER SHIT HERE BRO
                if self.isPlaying:
                    time.sleep(.1)
                else:
                    time.sleep(.1)

                if pygame.mixer.music.get_pos() < 0:
                    break
            
                self.__func_return(pygame.mixer.music.get_pos(), pygame.mixer.music.get_volume())

            if self.repeat == 0 and self.isPlaying:
                pygame.mixer.music.stop()
                self.__exit = True
                break

            if self.repeat == 1 and self.isPlaying:
                self.index = 0
                self._playSong()
            
            elif self.repeat == 2 and self.isPlaying:
                self.current_file_playing = self.songs_list[self.index]
                self._playSong()
                self.index += 1
                
                if self.index == len(self.songs_list):
                    self.index = 0

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
            self.volume = round(self.volume - .01, 4)
            pygame.mixer.music.set_volume(self.volume)
    
    def higher_volume(self) -> None:
        if self.volume < 1:
            self.volume = round(self.volume + .01, 4)
            pygame.mixer.music.set_volume(self.volume)
    
    def get_full_lenght(self) -> int:
        return int(self.current_song_length)

    def stop(self) -> None:
       pygame.mixer.music.stop()
       self.__exit = True
       self.isPlaying = False
