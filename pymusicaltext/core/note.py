from typing import List

import mido

from .midiunit import MidiUnit


class Note(MidiUnit):
    def __init__(self, note: str, octave: int, volume: int):
        self.__note = self.__decode_note(note)
        self.__octave = octave
        self.__volume = volume

    def generate_message(self) -> List[mido.Message]:
        """
        this "plays" the note, returning a list of 2 elements
        with the on/off messages
        important to note: velocity is the "loudness" of the song
        """
        # volume needs to be decreased by one since we are using 1-128
        # while midi uses 0-127
        return [
            mido.Message(
                "note_on",
                note=self.__note + self.__octave,
                velocity=self.__volume - 1,
                time=60,
            ),
            mido.Message(
                "note_off",
                note=self.__note + self.__octave,
                velocity=self.__volume - 1,
                time=0,
            ),
        ]

    def __decode_note(self, note: str) -> int:
        """
        this function will decode the note, a string, to the midi format
        """
        raise NotImplementedError("TODO")
