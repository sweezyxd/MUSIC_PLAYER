import pyaudio as pa
import wave
import 
from time import sleep
from threading import Thread

def playAudio(audio_file):
    wf = wave.open(audio_file, "rb")
    p = pa.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate=wf.getframerate(), output=True)

    chunk_size = 1024
    data = wf.readframes(chunk_size)
    n = 0
    while True:
        stream.write(data)
        data = wf.readframes(chunk_size)
    print("stopped")
    sleep(10)

    
    stream.stop_stream()
    stream.close()

    p.terminate()


playAudio("wavs/test.wav")


class MusicPlayer:
    def __init__(self) -> None:
        self.songplaying = ""
        self.wf, self.stream = None, None

    def play(self, song_path):
        # LOADING THE SONG
        wf = wave.open(audio_)

