from typing import List

import mido

from .midiunit import MidiUnit
from .midiinfo import BasicMidiInfo


class Note(MidiUnit):
    def __init__(self, note: str, player_info: BasicMidiInfo):
        self.__note = self.__decode_note(note)
        self.__info = player_info

    def generate_message(self) -> List[mido.Message]:
        """
        this "plays" the note, returning a list of 2 elements
        with the on/off messages
        important to note: velocity is the "loudness" of the song
        """
        return [
            mido.Message(
                "note_on",
                note=self.__note + self.__info.octave,
                velocity=self.__info.volume,
                time=60,
            ),
            mido.Message(
                "note_off",
                note=self.__note + self.__info.octave,
                velocity=self.__info.volume,
                time=0,
            ),
        ]

    def __decode_note(self, note: str) -> int:
        """
        this function will decode the note, a string, to the midi format
        """
        raise NotImplementedError("TODO")
