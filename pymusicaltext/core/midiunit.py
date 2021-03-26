import abc
from typing import List, Union
import mido


class MidiUnit(abc.ABC):
    @abc.abstractmethod
    def generate_message(self) -> Union[List[mido.Message], List[mido.MetaMessage]]:
        pass
