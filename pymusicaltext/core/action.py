from typing import Tuple, Union, List, Dict
from random import choice
from mido import MetaMessage
from .midiunit import MidiUnit


class Action(MidiUnit):
    def __init__(
        self, act: str, volume: int, octave: int, bpm: int, instrument: int
    ) -> None:
        self.__action = act
        self.__volume = volume
        self.__octave = octave
        self.__bpm = bpm
        self.__instrument = instrument

    def generate_message(self) -> List[MetaMessage]:
        # TODO: make a funciton that generates the meta message,
        # return a list for uniformity.
        raise NotImplementedError("TODO")

    def execute(self) -> Tuple[int, int, int, int]:
        """
        executes the action that the instance represents
        return a tuple with (volume, octave, bpm, instrument)
        with possible modifications
        the meta_message argument should be an empty list (but named)
        """
        to_run = self.__decode_action(self.__action)
        to_run()
        return (self.__volume, self.__octave, self.__bpm, self.__instrument)

    # TODO: come up with a way to check if meta_message needs to be written
    # and change it accordingly

    def __decode_action(self, act):
        raise NotImplementedError("TODO")

    def __increase_octave(self) -> None:
        self.__octave += 1
        if self.__octave > 7:
            self.__octave = 7

    def __decrease_octave(self) -> None:
        self.__octave -= 1
        if self.__octave < 0:
            self.__octave = 0

    def __increase_bpm(self) -> None:
        self.__bpm += 50

    def __decrease_bpm(self) -> None:
        self.__bpm -= 50
        if self.__bpm <= 4:
            # this is the lowest acceptable interger to have as bpm,
            # midi limitations with set_tempo
            self.__bpm = 4

    def __increase_volume(self) -> None:
        # the volume will NOT be duplicated for now, this would
        # cause the volume to be only at two states
        # this increases it by 10%
        self.__volume = round(self.__volume * 1.1)
        if self.__volume > 128:
            self.__volume = 128

    def __decrease_volume(self) -> None:
        # called decrease to maintain an uniformity,
        # but it resets the volume to 64
        self.__volume = 64

    def __change_instrument(self) -> None:
        # a random instrument from 0 to 127, as midi standard
        self.__instrument = choice(range(0, 128))
