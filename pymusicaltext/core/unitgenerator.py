from .note import Note
from .action import Action
import functools
from typing import Union


class MidiUnitGenerator:
    __last_token: str = ""

    def __init__(self, tok: str) -> None:
        self.__value = tok

    def generate(
        self,
    ) -> Union[functools.partial[Action], functools.partial[Note]]:
        note_tokens = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            " ",
            "?",
            ".",
        ]
        if self.__value in note_tokens:
            to_return = functools.partial(Note, self.__value)
        elif self.__value in "iou":
            if self.__last_token in note_tokens:
                self.__value = self.__last_token
                to_return = functools.partial(Note, self.__value)
            else:
                self.__value = " "
                to_return = functools.partial(Note, self.__value)
        else:
            to_return = functools.partial(Action, self.__value)
        self.__last_token = self.__value
        return to_return
