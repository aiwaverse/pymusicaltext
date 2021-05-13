from os.path import splitext
from typing import List, Union

import mido

from pymusicaltext.core.constants import (
    BPM_DEFAULT,
    INSTRUMENT_MIN,
    OCTAVE_MIN,
    VOLUME_DEFAULT,
)

from .unitgenerator import Generator
from .midiinfo import AdvancedMidiInfo
from .parser import Parser


class Player:
    def __init__(
        self,
        input_string: str = "",
        output_file_name: str = "",
        port: str = "",
    ) -> None:
        """
        initializes the basic parameters, the "medium" volume
        the basic bpm, volumes, initial notes, the first instrument from the
        midi table, middle octave
        plus with the file_name passed to the construction
        the basic octave is 3, to have the mid-note,
        as per usual of midi instruments
        """
        self.__info: AdvancedMidiInfo = AdvancedMidiInfo(
            OCTAVE_MIN, VOLUME_DEFAULT, INSTRUMENT_MIN, BPM_DEFAULT
        )
        self.__output_file_name = output_file_name
        self.__notes: List[
            Union[mido.MetaMessage, mido.Message]
        ] = self.__initial_midi_file
        self.__input_string = input_string
        self.__port = port
        self.__parse_input()

    def __parse_input(self) -> None:
        """
        parses the input string into the note/action tokens
        """
        tokens = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
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
        p = Parser(self.__input_string, tokens, True)
        self.__decoded_input = p.parse()

    def generate_notes(self) -> None:
        """
        this will use Generator to generate the notes
        that will go on the __notes list
        """
        for tok in self.__decoded_input:
            partial_element = Generator(tok).generate()
            element = partial_element(self.__info)
            self.__notes += element.generate_message()

    @property
    def input_string(self) -> str:
        return self.__input_string

    @input_string.setter
    def input_string(self, string: str) -> None:
        """
        loads a new string into the object
        useful for reading from a text box
        """
        self.__input_string = string
        self.__parse_input()

    @property
    def __initial_midi_file(self) -> List[mido.MetaMessage]:
        """
        a function that generates the basic meta_messages for the track
        """
        return [
            mido.MetaMessage("sequence_number", number=0, time=0),
            mido.MetaMessage(
                "track_name", name=splitext(self.__output_file_name)[0], time=0
            ),
        ]

    def calculate_end_time(self) -> int:
        """
        uses the time attribute on every note
        to calculate the end_of_track time
        """
        total_time = 0
        for msg in self.__notes:
            total_time += msg.time
        return total_time

    def generate_file(self) -> mido.MidiFile:
        """
         |s the notes to the file, adds an
        end_of_track meta message to the end too
        """
        save_file = mido.MidiFile()
        self.__notes.append(
            mido.MetaMessage("end_of_track", time=self.calculate_end_time())
        )
        save_file.tracks.append(self.__notes)
        save_file.save(filename=self.__output_file_name)
        return save_file

    def play_notes(self) -> None:
        file = mido.MidiFile()
        file.tracks.append(self.__notes)
        with mido.open_output(name=self.__port) as p:
            for msg in file.play():
                print(msg)
                p.send(msg)
