from functools import partial
from random import choice
from typing import Callable, Dict, List, Union

import mido

from pymusicaltext.core.constants import (
    BPM_STEP,
    INSTRUMENT_AGOGO,
    INSTRUMENT_CHURCH_ORGAN,
    INSTRUMENT_HARPSICHORD,
    INSTRUMENT_PAN_FLUTE,
    INSTRUMENT_TUBULAR_BELLS,
    MIDI_MAXIMUM,
    MIDI_MINIMUM,
    VOLUME_DEFAULT,
)

from .midiinfo import AdvancedMidiInfo
from .midiunit import MidiUnit


class Action(MidiUnit):
    def __init__(self, act: str, player_info: AdvancedMidiInfo) -> None:
        self.__action = act
        self.__info = player_info

    def generate_message(
        self,
    ) -> Union[List[mido.Message], List[mido.MetaMessage]]:
        # function that generates the message,
        # return a list for uniformity.
        self.__execute()
        if self.__action in ["?", ".", " "]:
            # changing octave or changing volume isn't done with messages
            return []
        return [mido.Message("program_change", program=self.__info.instrument)]

    def __execute(self) -> None:
        """
        executes the action that the instance represents
        alters the info (because of how python carries objects)
        this should be called in generate_message
        """
        to_run = self.__decode_action()
        to_run()

    def __decode_action(self) -> Callable[[], None]:
        """
        returns the function that the action needs to execute
        """
        # or at least one of them? As individuals?
        actions: Dict[str, Callable[[], None]] = {
            " ": self.__increase_volume,
            "?": self.__increase_octave,
            ".": self.__increase_octave,
            "!": partial(self.__change_instrument, INSTRUMENT_AGOGO),
            "O": partial(self.__change_instrument, INSTRUMENT_HARPSICHORD),
            "o": partial(self.__change_instrument, INSTRUMENT_HARPSICHORD),
            "I": partial(self.__change_instrument, INSTRUMENT_HARPSICHORD),
            "i": partial(self.__change_instrument, INSTRUMENT_HARPSICHORD),
            "U": partial(self.__change_instrument, INSTRUMENT_HARPSICHORD),
            "u": partial(self.__change_instrument, INSTRUMENT_HARPSICHORD),
            "\n": partial(self.__change_instrument, INSTRUMENT_TUBULAR_BELLS),
            ";": partial(self.__change_instrument, INSTRUMENT_PAN_FLUTE),
            ",": partial(self.__change_instrument, INSTRUMENT_CHURCH_ORGAN),
        }
        # if the action is none of above, it is a digit
        # default call defined to avoid too long line
        if self.__action.isdecimal():
            return partial(
                self.__change_instrument,
                int(self.__action) + self.__info.instrument,
            )
        return actions[self.__action]

    def __increase_octave(self) -> None:
        self.__info.octave += 1

    def __decrease_octave(self) -> None:
        self.__info.octave -= 1

    def __increase_bpm(self) -> None:
        self.__info.bpm += BPM_STEP

    def __decrease_bpm(self) -> None:
        self.__info.bpm -= BPM_STEP

    def __increase_volume(self) -> None:
        # duplicated the value of volume
        self.__info.volume *= 2

    def __decrease_volume(self) -> None:
        # called decrease to maintain an uniformity,
        # but it resets the volume to the default
        self.__info.volume = VOLUME_DEFAULT

    def __change_instrument(self, inst: int) -> None:
        # a random instrument from 0 to 127, as midi standard
        self.__info.instrument = inst
