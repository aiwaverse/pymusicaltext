import abc
import os


class InputForm(abc.ABC):
    """
    Class to control all forms of input on the program
    """
    @property
    @abc.abstractmethod
    def content(self) -> str:
        pass


class StringInput(InputForm):
    """
    StringInput is the most basic Input, just text
    """
    def __init__(self, content: str) -> None:
        self._content = content

    @property
    def content(self) -> str:
        return self._content


class FileInput(InputForm):
    """
    FileInput reads text from a file.
    If file does not exist, open will raise FileNotFoundError
    Nothing can be done on this class
    """
    def __init__(self, file_name: str) -> None:
        with open(file_name, encoding="utf-8", "r") as f:
            self._content = f.read()

    @property
    def content(self):
        return self._content
