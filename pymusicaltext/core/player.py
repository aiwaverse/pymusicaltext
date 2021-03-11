#%%
from os import environ
from typing import List, Union

import mido

from .action import Action
from .note import Note
from .parser import Parser

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame


class Player:
    def __init__(self, input_string: str, output_file_name: str) -> None:
        """
        initializes the basic parameters, the "medium" volume
        the basic bpm, volumes, initial notes, the first intrument from the midi table, middle octave
        plus with the file_name passed to the construction
        the basic octave is 3, to have the mid-note, as per usual of midi intruments
        """
        self.__volume: int = 64
        self.__bpm: int = 120
        self.__notes: List[
            Union[mido.MetaMessage, mido.Message]
        ] = self.__initial_midi_file()
        self.__instrument: int = 0
        self.__octave: int = 3
        self.__output_file_name = output_file_name
        self.__input = input_string
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
        p = Parser(self.__input, tokens)
        self.__decoded_input = p.parse()

    def __generate_notes(self) -> None:
        """
        this will use Note/Action to generate the notes that will go on the __notes list
        """
        raise NotImplementedError("TODO")

    def load_string(self, string: str) -> None:
        """
        loads a new string into the object
        useful for reading from a text box
        """
        self.__input = string
        self.__parse_input()

    def __initial_midi_file(self) -> mido.Message:
        """
        a function that generates the basic meta_messages for the track
        """
        return [
            mido.MetaMessage("sequence_number", number=0, time=0),
            mido.MetaMessage("track_name", name="pymusicaltext generated file", time=0),
        ]

    def __change_instrument(self) -> mido.MetaMessage:
        """
        this functions generates a meta-message that changes the midi instrument of the track
        """
        return mido.MetaMessage("program_change", program=self.__instrument)

    def __calculate_end_time(self) -> int:
        """
        uses the time attribute on every note to calculate the end_of_track time
        """
        total_time = 0
        for msg in self.__notes:
            total_time += msg.time
        return total_time

    def __write_notes_to_file(self) -> None:
        """
        writes the notes to the file, adds an end_of_track meta message to the end too
        """
        save_file = mido.MidiFile()
        self.__notes.append(
            mido.MetaMessage("end_of_track", time=self.__calculate_end_time())
        )
        save_file.tracks.append(self.__notes)
        save_file.save(filename=self.__output_file_name)

    @staticmethod
    def play_midi_file(midi_file: str) -> None:
        """
        stream music with mixer.music module in blocking manner
        this will stream the sound from disk while playing
        """
        clock = pygame.time.Clock()
        try:
            pygame.mixer.music.load(midi_file)
        except pygame.error:
            print(f"File {midi_file} not found, error {pygame.get_error()}")
            return
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            # check if playback has finished
            clock.tick(30)


# %%
