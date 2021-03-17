from os import environ
from os.path import splitext
from typing import List, Union

import mido

from pymusicaltext.core.constants import (
    BPM_MIN,
    BPM_MIN,
    INSTRUMENT_MIN,
    OCTAVE_MIN,
    VOLUME_DEFAULT,
)

from .action import Action
from .midiinfo import AdvancedMidiInfo
from .note import Note
from .parser import Parser


class Player:
    def __init__(
        self, input_string: str, output_file_name: str, port: str
    ) -> None:
        """
        initializes the basic parameters, the "medium" volume
        the basic bpm, volumes, initial notes, the first intrument from the
        midi table, middle octave
        plus with the file_name passed to the construction
        the basic octave is 3, to have the mid-note,
        as per usual of midi intruments
        """
        self.__info: AdvancedMidiInfo = AdvancedMidiInfo(
            OCTAVE_MIN, VOLUME_DEFAULT, INSTRUMENT_MIN, BPM_MIN
        )
        self.__output_file_name = output_file_name
        self.__notes: List[
            Union[mido.MetaMessage, mido.Message]
        ] = self.__initial_midi_file()
        self.__input_string = input_string
        self.__port = port
        self.__parse_input()

    def __parse_input(self) -> None:
        """
        parses the input string into the note/action tokens
        """
        tokens = [
            "bpm+",
            "bpm-",
            "t+",
            "t-",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            " ",
            "+",
            "-",
            "o",
            "i",
            "u",
            "?",
            ".",
            "\n",
        ]
        p = Parser(self.__input, tokens, return_not_matched=False)
        self.__decoded_input = p.parse()

    def __generate_notes(self) -> None:
        """
        this will use Note/Action to generate the notes
        that will go on the __notes list
        """
        note_tokens = [
            "a",
            "i",
            "o",
            "u",
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
        previous_tok = ""
        for tok in self.__decoded_input:
            if tok in note_tokens:
                # tok is a note
                if tok in "iou" and previous_tok in note_tokens:
                    curr = Note(tok, self.__info)
                else:
                    curr = Note(" ", self.__info)
            else:
                # tok is an action
                curr = Action(tok, self.__info)
            self.__notes += curr.generate_message()

    @property
    def input_string(self) -> str:
        return self.__input_string

    @input_string.setter
    def input_string(self, string: str) -> None:
        """
        loads a new string into the object
        useful for reading from a text box
        """
        self.__input = string
        self.__parse_input()

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

    def __calculate_end_time(self) -> int:
        """
        uses the time attribute on every note
        to calculate the end_of_track time
        """
        total_time = 0
        for msg in self.__notes:
            total_time += msg.time
        return total_time

    def generate_file(self) -> None:
        """
        writes the notes to the file, adds an
        end_of_track meta message to the end too
        """
        save_file = mido.MidiFile()
        self.__notes.append(
            mido.MetaMessage("end_of_track", time=self.__calculate_end_time())
        )
        save_file.tracks.append(self.__notes)
        save_file.save(filename=self.__output_file_name)

    def play_notes(self) -> None:
        file = mido.MidiFile()
        file.tracks[0] = self.__notes
        with mido.open_output(name=self.__port) as p:
            for msg in file.play():
                p.send(msg)
