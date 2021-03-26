from typing import List, Dict

import mido

from .midiunit import MidiUnit
from .midiinfo import BasicMidiInfo

from .constants import (
    NOTE_A,
    NOTE_B,
    NOTE_C,
    NOTE_D,
    NOTE_E,
    NOTE_F,
    NOTE_G,
    NOTE_DURATION,
)


class Note(MidiUnit):
    def __init__(self, note: str, player_info: BasicMidiInfo):
        self.__note = self.__decode_note(note)
        # self.__note = 0
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
                time=NOTE_DURATION,
            ),
            mido.Message(
                "note_off",
                note=self.__note + self.__info.octave,
                velocity=self.__info.volume,
                time=0,
            ),
        ]

    def test(self) -> None:
        print("Entering Note Test!")
        print("Incrementing volume by 10 and Octave by 2.")
        self.__info.volume += 10
        self.__info.octave += 2

    @staticmethod
    def __decode_note(note: str) -> int:
        """
        this function will decode the note, a string, to the midi format
        """
        note_dict: Dict[str, int] = {
            "C": NOTE_C,
            "D": NOTE_D,
            "E": NOTE_E,
            "F": NOTE_F,
            "G": NOTE_G,
            "A": NOTE_A,
            "B": NOTE_B,
        }
        return note_dict[note.upper()]
