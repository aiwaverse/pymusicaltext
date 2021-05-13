import os

import PySimpleGUI as sg
from PySimpleGUI import Button, Text
from PySimpleGUI.PySimpleGUI import FileSaveAs

import pymusicaltext.gui.constants as gui_constants

dir_path = os.path.dirname(os.path.realpath(__file__))

START_IMG = os.path.join(dir_path, "assets", "icons", "play.png")
STOP_IMG = os.path.join(dir_path, "assets", "icons", "stop.png")
PAUSE_IMG = os.path.join(dir_path, "assets", "icons", "pause.png")


def btn(title: str, key=None) -> Button:
    return sg.Button(
        title,
        border_width=0,
        pad=(0, 0),
        font=("Ubuntu", 12),
        size=(20, 1),
        key=key,
    )


def image_btn(key: str, file: str) -> Button:
    return sg.Button(
        border_width=0,
        button_color=("#335267", "#335267"),
        key=key,
        image_filename=file,
        image_size=(25, 25),
        image_subsample=4,
    )


def text(label: str, font_weight="bold", key="", size=(None, None)) -> Text:
    return sg.Text(
        label,
        size=size,
        text_color="#fff",
        font=("Roboto", 11, font_weight),
        key=key,
    )


class Layout:
    def __init__(self, title):
        self.title = title

    def make_gui(self) -> sg.Window:
        sg.theme("Dark Blue 2")

        input_text_col = sg.pin(
            sg.Column(
                [
                    [text("Type a Text")],
                    [
                        sg.Multiline(
                            font=("Ubuntu", 11),
                            size=(40, 10),
                            key=gui_constants.IN_TEXT_INPUT,
                            focus=True,
                        ),
                    ],
                    [text("Or choose a file:")],
                    [
                        sg.Input(
                            size=(25, 20),
                            font=("Ubuntu", 12),
                            key=gui_constants.IN_FILE_INPUT,
                        ),
                        sg.FileBrowse(font=("Ubuntu", 12)),
                    ],
                ],
                size=(370, 300),
                element_justification="left",
                vertical_alignment="top",
            )
        )

        file_name_col = sg.pin(
            sg.Column(
                [
                    [text("Nome do arquivo:")],
                    [
                        sg.Input(
                            font=("Ubuntu", 11),
                            size=(40, 10),
                            key=gui_constants.IN_FILE_NAME,
                        ),
                    ],
                    [btn("Generate music")],
                ],
                size=(370, 300),
                element_justification="left",
                vertical_alignment="top",
            )
        )

        file_info_col = sg.pin(
            sg.Column(
                [
                    [text("Dados da arquivo:")],
                    [
                        text("Nome:", "normal"),
                        text(
                            "Not load",
                            "normal",
                            gui_constants.TEXT_FILE_NAME,
                            size=(30, 1),
                        ),
                    ],
                    [
                        text("Duração:", "normal"),
                        text(
                            "",
                            "normal",
                            gui_constants.TEXT_DURATION,
                            size=(30, 1),
                        ),
                    ],
                    [
                        text("Data de Criação:", "normal"),
                        text(
                            "",
                            "normal",
                            gui_constants.TEXT_CREATED_AT,
                            size=(30, 1),
                        ),
                    ],
                ],
                size=(370, 120),
                element_justification="left",
                vertical_alignment="top",
                visible=False,
                key=gui_constants.FILE_INFO_SECTION,
            )
        )

        player_col_bg = "#335267"

        player_col = sg.pin(
            sg.Column(
                [
                    [
                        sg.Text(
                            "",
                            size=(30, 1),
                            font=("Helvetica", 14),
                            key="output",
                            background_color=player_col_bg,
                        )
                    ],
                    [
                        sg.ProgressBar(
                            100,
                            orientation="h",
                            size=(25, 10),
                            key="progressbar",
                            bar_color=("#fff", "#000"),
                            border_width=1,
                        )
                    ],
                    [
                        image_btn("Start", START_IMG),
                        sg.Text(" " * 2, background_color=player_col_bg),
                        image_btn("Pause", PAUSE_IMG),
                        sg.Text(" " * 2, background_color=player_col_bg),
                        image_btn("Stop", STOP_IMG),
                        sg.Text(" " * 4, background_color=player_col_bg),
                        sg.Slider(
                            range=(0, 10),
                            default_value=10,
                            size=(10, 10),
                            orientation="horizontal",
                            font=("Helvetica", 10),
                            background_color="#335267",
                        ),
                    ],
                ],
                size=(320, 100),
                element_justification="left",
                vertical_alignment="top",
                background_color=player_col_bg,
                visible=False,
                key=gui_constants.PLAYER_SECTION,
            )
        )

        layout = [
            [
                sg.Text(
                    "Py Musical Text",
                    text_color="#fff",
                    font=("Roboto", 15, "bold"),
                )
            ],
            [input_text_col, file_name_col],
            [file_info_col, player_col],
            [sg.Exit(button_color="#dc3545")],
        ]

        return sg.Window(self.title, layout)
