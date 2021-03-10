#%%
import pygame
import mido

class Player:
    def __init__(self) -> None:
        self.__volume = 64
        self.__bpm = 120
        self.__notes = []
        self.__instrument = 0
    
    @staticmethod
    def play_midi_file(midi_file: str) -> None:
            """
            stream music with mixer.music module in blocking manner
            this will stream the sound from disk while playing
            """
            clock = pygame.time.Clock()
            try:
                pygame.mixer.music.load(midi_file)
            except pygame.error:
                print(f"File {midi_file} not found, error {pygame.get_error()}")
                return
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                # check if playback has finished
                clock.tick(30)
# %%
