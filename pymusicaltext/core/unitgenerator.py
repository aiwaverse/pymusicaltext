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
        self.__value = tok

    def generate(self) -> Callable[[BasicMidiInfo], MidiUnit]:
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
        ]
        action_tokens = [
            " ",
            "!",
            "O",
            "o",
            "I",
            "i",
            "U",
            "u",
            "\n",
            "?",
            ".",
            ";",
            ",",
        ]
        if self.__value in note_tokens:
            to_return = functools.partial(Note, self.__value)
        elif self.__value.isdecimal() or self.__value in action_tokens:
            to_return = functools.partial(Action, self.__value)
        else:
            # If the token is neither a note or an action
            # We start to tackle the repetition cases
            if self.__value == self.__last_token.lower():
                # Very directly, if the value is the same as the last note
                # but lowercase
                self.__value = self.__value.upper()
            elif (
                self.__value not in "abcdefg"
                and self.__last_token in note_tokens
            ):
                # Now we tackle if the letter is another consonant
                # BUT it's not a "lower case note"
                self.__value = self.__last_token
            else:
                self.__value = ""
            to_return = functools.partial(Note, self.__value)
        Generator.__last_token = self.__value
        return to_return
