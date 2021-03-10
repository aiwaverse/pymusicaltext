#%%
from os import environ
from typing import Union

import mido

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame


class Player:
    def __init__(self) -> None:
        """
        initializes the basic parameters, the "medium" volume
        the basic bpm, no notes, and the first intrument from the midi table
        the basic octave is 3, to have the mid-note, as per usual of midi intruments
        """
        self.__volume: int = 64
        self.__bpm: int = 120
        self.__notes: Union[mido.MetaMessage, mido.Message] = []
        self.__instrument: int = 0
        self.__octave: int = 3

    def __change_instrument(self) -> mido.MetaMessage:
        """
        this functions generates a meta-message that changes the midi instrument of the track
        """
        return mido.MetaMessage("program_change", program=self.__instrument)

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
