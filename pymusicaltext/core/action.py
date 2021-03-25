from pymusicaltext.core.constants import (
    BPM_STEP,
    MIDI_MAXIMUM,
    MIDI_MINIMUM,
    VOLUME_DEFAULT,
)
from random import choice
from typing import Callable, Dict, List, Union

import mido

from .midiinfo import AdvancedMidiInfo
from .midiunit import MidiUnit


class Action(MidiUnit):
    def __init__(self, act: str, player_info: AdvancedMidiInfo) -> None:
        self.__action = act
        self.__info = player_info

    def generate_message(
        self,
    ) -> Union[List[mido.Message], List[mido.MetaMessage]]:
        # funciton that generates the message,
        # return a list for uniformity.
        self.__execute()
        return_messages: Dict[str, List[mido.MetaMessage]] = {
            "bpm+": [
                mido.MetaMessage(
                    "set_tempo", tempo=mido.tempo2bpm(self.__info.bpm)
                )
            ],
            "bpm-": [
                mido.MetaMessage(
                    "set_tempo", tempo=mido.tempo2bpm(self.__info.bpm)
                )
            ],
            # for some reason, program change is not a MetaMessage, blame mido
            "\n": [
                mido.Message("program_change", program=self.__info.instrument)
            ],
        }
        return return_messages.get(self.__action, [])

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
        returns the function taht the action needs to execute
        """
        actions: Dict[str, Callable[[], None]] = {
            "bpm+": self.__increase_bpm,
            "bpm-": self.__decrease_bpm,
            "\n": self.__change_instrument,
            "T+": self.__increase_octave,
            "T-": self.__decrease_octave,
            "+": self.__increase_volume,
            "-": self.__decrease_volume,
        }
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

    def __change_instrument(self) -> None:
        # a random instrument from 0 to 127, as midi standard
        self.__info.instrument = choice(range(MIDI_MINIMUM, MIDI_MAXIMUM + 1))

    def test(self) -> None:
        print("Entering Action Test function!")
        print(
            "Decreasing volume by 20, Octave by 2, Increasing bpm by 150, and \
            setting instrument to 78."
        )
        self.__info.volume -= 20
        self.__info.octave -= 2
        self.__info.bpm += 150
        self.__info.instrument = 78
