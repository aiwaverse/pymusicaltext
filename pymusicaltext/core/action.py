from random import choice
from typing import List, Tuple

import mido

from .midiinfo import AdvancedMidiInfo
from .midiunit import MidiUnit


class Action(MidiUnit):
    def __init__(self, act: str, player_info: AdvancedMidiInfo) -> None:
        self.__action = act
        self.__info = player_info

    def generate_message(self) -> List[mido.MetaMessage]:
        # TODO: make a funciton that generates the meta message,
        # return a list for uniformity.
        raise NotImplementedError("TODO")

    def __execute(self) -> None:
        """
        executes the action that the instance represents
        alters the info (because of how python carries objects)
        this should be called in generate_message
        """
        to_run = self.__decode_action(self.__action)
        to_run()

    # TODO: come up with a way to check if meta_message needs to be written
    # and change it accordingly

    def __decode_action(self, act):
        raise NotImplementedError("TODO")

    def __increase_octave(self) -> None:
        self.__info.octave += 1

    def __decrease_octave(self) -> None:
        self.__info.octave -= 1

    def __increase_bpm(self) -> None:
        self.__info.bpm += 50

    def __decrease_bpm(self) -> None:
        self.__info.bpm -= 50
        if self.__info.bpm <= 4:
            # this is the lowest acceptable interger to have as bpm,
            # midi limitations with set_tempo
            self.__info.bpm = 4

    def __increase_volume(self) -> None:
        # the volume will NOT be duplicated for now, this would
        # cause the volume to be only at two states
        # this increases it by 10%
        self.__info.volume = round(self.__info.volume * 1.1)
        if self.__info.volume > 128:
            self.__info.volume = 128

    def __decrease_volume(self) -> None:
        # called decrease to maintain an uniformity,
        # but it resets the volume to 64
        self.__info.volume = 64

    def __change_instrument(self) -> None:
        # a random instrument from 0 to 127, as midi standard
        self.__info.instrument = choice(range(0, 128))
