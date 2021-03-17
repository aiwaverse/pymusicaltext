import abc
from typing import List, Union
from mido import Message, MetaMessage


class MidiUnit(abc.ABC):
    @abc.abstractmethod
    def generate_message(self) -> Union[List[Message], List[MetaMessage]]:
        pass
