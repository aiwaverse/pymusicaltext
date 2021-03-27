from .note import Note
from .action import Action
import functools
from typing import Callable, Union
from .midiinfo import BasicMidiInfo, AdvancedMidiInfo
from .midiunit import MidiUnit


class Generator:
    """
    A class to control the generation of MidiUnits
    """

    __last_token: str = ""

    def __init__(self, tok: str) -> None:
        self.__value = tok.upper()

    def generate(
        self,
    ) -> Callable[[BasicMidiInfo], MidiUnit]:
        """
        this function ideally should return a
        partially applied MidiUnit constructor
        however, partial is invariant, so we had to
        resort to using Union again
        """
        note_tokens = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            " ",
            "?",
            ".",
        ]
        if self.__value in note_tokens:
            to_return = functools.partial(Note, self.__value)
        elif self.__value in "iou":
            if Generator.__last_token in note_tokens:
                self.__value = Generator.__last_token
                to_return = functools.partial(Note, self.__value)
            else:
                self.__value = " "
                to_return = functools.partial(Note, self.__value)
        else:
            to_return = functools.partial(Action, self.__value)
        Generator.__last_token = self.__value
        return to_return
