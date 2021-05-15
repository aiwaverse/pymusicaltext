"""
The interface module contains a single
class, the GUI, which is used on the program
"""
import os
import shutil
import time
from datetime import date
from typing import Optional, Tuple

import PySimpleGUI as sg
from mido.midifiles.midifiles import MidiFile
from pymusicaltext.core.input_form import FileInput, StringInput
from pymusicaltext.core.player import Player
from pymusicaltext.gui.constants import (
    DOWNLOAD_BUTTON,
    EXIT,
    FILE_INFO_SECTION,
    GENERATE_MUSIC,
    IN_FILE_INPUT,
    IN_FILE_NAME,
    IN_TEXT_INPUT,
    START,
    PAUSE,
    STOP,
    PLAYER_SECTION,
    PROGRESS_BAR,
    TEXT_CREATED_AT,
    TEXT_DURATION,
    TEXT_FILE_NAME,
    VOLUME_CHANGE,
)


class GUI:
    """
    The GUI for the PyMusicalText program
    """

    def __init__(self, title: str) -> None:
        """
        Initialized the GUI with the title given
        """
        self.__title = title
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.__start_img = os.path.join(
            dir_path, "assets", "icons", "play.png"
        )
        self.__stop_img = os.path.join(dir_path, "assets", "icons", "stop.png")
        self.__pause_img = os.path.join(
            dir_path, "assets", "icons", "pause.png"
        )
        self.__window = self._create_gui()
        self.__player = None
        self.__midi_file: Optional[MidiFile] = None
        self.__current_progress = 0
        self.__playing = False
        self.__song_loaded = False
        self.__last_progress_bar_change = None

    @property
    def file_name(self) -> str:
        """
        Property for the file name loaded
        """
        return_name = ".tmp/"
        return_name += self.__player.file_correct_name(
            self.__midi_file.filename
        )
        return_name += ".wav"
        return return_name

    def __time_unit(self) -> float:
        """
        Time unit to be used on the progress bar
        """
        if round(self.__midi_file.length) == 0:
            return 100
        return 100 / round(self.__midi_file.length)

    def __initialize_player(self) -> None:
        """
        Initalizes the player by generating the notes and the file
        """
        self.__player.generate_notes()
        self.__midi_file = self.__player.generate_file()

    def __update_player_values(self) -> None:
        """
        Updates the player values after a new song is loaded
        """
        self.window[TEXT_FILE_NAME].update(f"{self.__midi_file.filename}.wav")
        self.window[TEXT_DURATION].update(f"{self.__midi_file.length}s")
        self.window[TEXT_CREATED_AT].update(date.today().strftime("%d/%m/%Y"))
        self.window[PROGRESS_BAR].update(0)
        self.__current_progress = 0
        self.__song_loaded = False
        self.__playing = False
        self.__last_progress_bar_change = None

    def __delete_generated_files(self) -> None:
        if self.__midi_file:
            os.remove(f".tmp/{self.__midi_file.filename}.wav")
            os.remove(f".tmp/{self.__midi_file.filename}.mid")

    def close_player(self):
        """
        Removes temporary files, closes the window and
        deletes the attribute.
        """
        self.__delete_generated_files()
        self.window.close()

    def update_progress_bar(self) -> None:
        """
        Updates the progress bar of the song with the current progress.
        """
        if not self.__last_progress_bar_change:
            self.__last_progress_bar_change = time.time()
        time_dif = time.time() - self.__last_progress_bar_change
        if time_dif >= 1:
            self.__current_progress += self.__time_unit() * round(time_dif)
            self.window[PROGRESS_BAR].update(self.__current_progress)
            self.__last_progress_bar_change = time.time()

    @property
    def playing(self) -> bool:
        """
        Returns if a song is current being played.
        """
        return self.__playing

    @property
    def song_loaded(self) -> bool:
        """
        Returns if a song is current loaded.
        """
        return self.__song_loaded

    def download_file(self, path: str) -> None:
        """
        Downloads the .wav file into the path given
        """
        shutil.copy(self.file_name, path)

    def change_volume(self, vol: float) -> None:
        """
        Changes the volume of the song being played with vol
        Divided by 10 because of how pygame uses volume
        """
        self.__player.change_volume(vol / 10)

    def start_song(self) -> None:
        """
        Starts the song on the player.
        """
        if not self.__playing:
            if not self.song_loaded:
                self.__player.load_and_play_file(self.file_name)
                self.__song_loaded = True
                self.__current_progress = self.__time_unit()
            else:
                self.__player.play_song()
            self.__last_progress_bar_change = time.time()
        self.__playing = True

    def pause_song(self) -> None:
        """
        Pauses the song on the player.
        """
        self.__player.pause_song()
        self.__playing = False

    def stop_song(self) -> None:
        """
        Stops the song on the player (pauses and return to beggining)
        """
        self.__player.stop_song()
        self.__playing = False
        self.window[PROGRESS_BAR].update(0)
        self.__current_progress = self.__time_unit()

    @staticmethod
    def check_file_name(file_name: str) -> bool:
        """
        Checks if the file name ends on .mid
        """
        if not file_name.endswith(".mid"):
            sg.popup_error("O nome do arquivo deve terminar em .mid")
            return False
        return True

    def create_player(self) -> None:
        """
        Creates the player, if a file is provided, uses the file.
        Otherwise, uses the input string.
        """
        _, values = self.read()
        if values[IN_FILE_INPUT]:
            try:
                text = FileInput(values[IN_FILE_INPUT])
            except FileNotFoundError:
                sg.popup_error("Erro de leitura do arquivo, verifique se o mesmo existe.")
                raise ValueError(
                    "Erro de leitura do arquivo, verifique se o mesmo existe."
                )
        else:
            text = StringInput(values[IN_TEXT_INPUT])
        if not self.check_file_name(values[IN_FILE_NAME]):
            raise ValueError("Nome do arquivo incorreto.")
        self.__delete_generated_files()
        self.__player = Player(text.content, values[IN_FILE_NAME])
        self.__initialize_player()
        self.__update_player_values()

    def make_full_gui_visible(self) -> None:
        """
        Makes the full GUI visible for the user.
        """
        self.window[FILE_INFO_SECTION].update(visible=True)
        self.window[PLAYER_SECTION].update(visible=True)

    def empty_input(self) -> bool:
        """
        Tests to see if the inputs are empty.
        No file name is also an empty input.
        """
        _, values = self.read()
        if not values[IN_FILE_INPUT] and values[IN_TEXT_INPUT] == "\n":
            return True
        if not values[IN_FILE_NAME]:
            return True
        return False

    @property
    def window(self):
        """
        Returns the GUI window
        """
        return self.__window

    def read(self, timeout: int = 0):
        """
        Reads the GUI window
        """
        return self.window.read(timeout=timeout)

    @staticmethod
    def _make_button(title: str, key=None) -> sg.Button:
        """
        Makes a button with predefined attributes
        """
        return sg.Button(
            title,
            border_width=0,
            pad=(0, 0),
            font=("Ubuntu", 12),
            size=(20, 1),
            key=key,
        )

    @staticmethod
    def _make_text(
        label: str,
        font_weight="bold",
        key="",
        size: Tuple[Optional[int], Optional[int]] = (None, None),
    ) -> sg.Text:
        """
        Makes a text with predefined attributes
        """
        return sg.Text(
            label,
            size=size,
            text_color="#fff",
            font=("Roboto", 11, font_weight),
            key=key,
        )

    @staticmethod
    def _make_button_with_image(key: str, file: str) -> sg.Button:
        """
        Makes a button with the image given on file.
        """
        return sg.Button(
            border_width=0,
            button_color=("#335267", "#335267"),
            key=key,
            image_filename=file,
            image_size=(25, 25),
            image_subsample=4,
        )

    def _create_gui(self):
        """
        Creates the GUI with the right attributes
        """
        sg.theme("DarkBlue17")
        layout = [
            [
                sg.Text(
                    "PyMusicalText",
                    text_color="#fff",
                    font=("Roboto", 15, "bold"),
                )
            ],
            [self.input_text_col, self.file_name_col],
            [self.file_info_col, self.player_col],
            [sg.Exit("Sair", button_color="#dc3545", key=EXIT)],
        ]

        return sg.Window(self.__title, layout)

    @property
    def file_name_col(self) -> sg.Column:
        """
        Property for the file name collumn
        """
        return sg.pin(
            sg.Column(
                [
                    [self._make_text("Nome do arquivo:")],
                    [
                        sg.Input(
                            font=("Ubuntu", 11),
                            size=(40, 10),
                            key=IN_FILE_NAME,
                        ),
                    ],
                    [self._make_button("Gerar música", key=GENERATE_MUSIC)],
                ],
                size=(370, 300),
                element_justification="left",
                vertical_alignment="top",
            )
        )

    @property
    def input_text_col(self) -> sg.Column:
        """
        Property for the input text column
        """
        return sg.pin(
            sg.Column(
                [
                    [self._make_text("Digite um texto:")],
                    [
                        sg.Multiline(
                            font=("Ubuntu", 11),
                            size=(40, 10),
                            key=IN_TEXT_INPUT,
                            focus=True,
                        ),
                    ],
                    [self._make_text("Ou escolha um arquivo:")],
                    [
                        sg.Input(
                            size=(25, 20),
                            font=("Ubuntu", 12),
                            key=IN_FILE_INPUT,
                        ),
                        sg.FileBrowse(font=("Ubuntu", 12)),
                    ],
                ],
                size=(370, 300),
                element_justification="left",
                vertical_alignment="top",
            )
        )

    @property
    def file_info_col(self) -> sg.Column:
        """
        Property for the file information column
        """
        return sg.pin(
            sg.Column(
                [
                    [self._make_text("Dados da arquivo:")],
                    [
                        self._make_text("Nome:", "normal"),
                        self._make_text(
                            "Not load",
                            "normal",
                            TEXT_FILE_NAME,
                            size=(30, 1),
                        ),
                    ],
                    [
                        self._make_text("Duração:", "normal"),
                        self._make_text(
                            "",
                            "normal",
                            TEXT_DURATION,
                            size=(30, 1),
                        ),
                    ],
                    [
                        self._make_text("Data de Criação:", "normal"),
                        self._make_text(
                            "",
                            "normal",
                            TEXT_CREATED_AT,
                            size=(30, 1),
                        ),
                    ],
                    [self._make_button("Baixar", key=DOWNLOAD_BUTTON)],
                ],
                size=(370, 150),
                element_justification="left",
                vertical_alignment="top",
                visible=False,
                key=FILE_INFO_SECTION,
            )
        )

    @property
    def player_col(self) -> sg.Column:
        """
        Property for the music player column
        """
        return sg.pin(
            sg.Column(
                [
                    [
                        sg.Text(
                            "",
                            size=(30, 1),
                            font=("Helvetica", 14),
                            key="output",
                            background_color="#335267",
                        )
                    ],
                    [
                        sg.ProgressBar(
                            100,
                            orientation="h",
                            size=(25, 10),
                            key=PROGRESS_BAR,
                            bar_color=("#fff", "#000"),
                            border_width=1,
                        )
                    ],
                    [
                        self._make_button_with_image(START, self.__start_img),
                        sg.Text(" " * 2, background_color="#335267"),
                        self._make_button_with_image(PAUSE, self.__pause_img),
                        sg.Text(" " * 2, background_color="#335267"),
                        self._make_button_with_image(STOP, self.__stop_img),
                        sg.Text(" " * 4, background_color="#335267"),
                        sg.Slider(
                            range=(0, 10),
                            default_value=10,
                            size=(10, 10),
                            orientation="horizontal",
                            font=("Helvetica", 10),
                            background_color="#335267",
                            key=VOLUME_CHANGE,
                            enable_events=True,
                            disable_number_display=True,
                        ),
                    ],
                ],
                size=(320, 100),
                element_justification="center",
                vertical_alignment="top",
                background_color="#335267",
                visible=False,
                key=PLAYER_SECTION,
            )
        )
