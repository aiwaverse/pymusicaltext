from os.path import splitext
import os
from typing import List, Union
import mido
import pygame
from midi2audio import FluidSynth

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
        output_file_name: str = ""
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
        self.__parse_input()
        pygame.init()
        if not os.path.exists(".tmp"):
            os.mkdir(".tmp")

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

    @staticmethod
    def file_correct_name(name: str) -> str:
        if name.endswith(".midi"):
            return name.replace(".midi", "")
        if name.endswith(".mid"):
            return name.replace(".mid", "")
        else:
            return name

    def generate_file(self) -> mido.MidiFile:
        """
         |s the notes to the file, adds an
        end_of_track meta message to the end too
        """
        name = self.file_correct_name(self.__output_file_name)
        save_file = mido.MidiFile()
        save_file.filename = name
        save_file.tracks.append(self.__notes)
        save_file.save(filename=f".tmp/{name}.mid")
        FluidSynth().midi_to_audio(
            f".tmp/{name}.mid", f".tmp/{name}.wav"
        )
        return save_file

    @staticmethod
    def load_and_play_file(file: str) -> None:
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

    @staticmethod
    def play_song() -> None:
        pygame.mixer.music.play()

    @staticmethod
    def pause_song() -> None:
        pygame.mixer.music.pause()

    @staticmethod
    def stop_song() -> None:
        pygame.mixer.music.stop()

    @staticmethod
    def change_volume(vol: int) -> None:
        pygame.mixer.music.set_volume(vol)
