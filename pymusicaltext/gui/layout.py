import os

import PySimpleGUI as sg
from PySimpleGUI import Button, Text

dir_path = os.path.dirname(os.path.realpath(__file__))

START_IMG = os.path.join(dir_path, 'assets', 'icons', 'play.png')
STOP_IMG = os.path.join(dir_path, 'assets', 'icons', 'stop.png')
PAUSE_IMG = os.path.join(dir_path, 'assets', 'icons', 'pause.png')


def btn(title: str) -> Button:
    return sg.Button(title, border_width=0, pad=(0, 0), font=("Ubuntu", 12), size=(20, 1))


def image_btn(key: str, file: str) -> Button:
    return sg.Button(border_width=0, button_color=('#335267', '#335267'),
                     key=key, image_filename=file, image_size=(25, 25), image_subsample=4)


def text(label: str, font_weight="bold") -> Text:
    return sg.Text(label, text_color="#fff", font=("Roboto", 11, font_weight))


class Layout:

    def __init__(self, title):
        self.title = title

    def make_gui(self) -> sg.Window:
        sg.theme('Dark Blue 2')

        input_text_col = sg.Column([
            [text("Type a Text")],
            [
                sg.Multiline(
                    font=("Ubuntu", 11),
                    size=(40, 10),
                    default_text="Decoded song goes here...",
                    key="in",
                    focus=True,
                ),
            ],
            [text("Or choose a file:")],
            [sg.Input(size=(25, 20), font=("Ubuntu", 12), key="file"),
             sg.FileBrowse(font=("Ubuntu", 12))],
        ], size=(370, 300), element_justification="left", vertical_alignment="top")

        file_name_col = sg.Column([
            [text("Nome do arquivo:")],
            [
                sg.Input(
                    font=("Ubuntu", 11),
                    size=(40, 10),
                    key="file_name",
                ),
            ],
            [btn('Generate music')],

        ], size=(370, 300), element_justification="left", vertical_alignment="top")

        file_info_col = sg.Column([
            [text("Dados da arquivo:")],
            [text("Nome:", "normal"), text("teste.mid", "normal")],
            [text("Duração:", "normal"), text("1m25s", "normal")],
            [text("Data de Criação:", "normal"), text("15/08/2021", "normal")],
        ], size=(370, 120), element_justification="left", vertical_alignment="top")

        player_col_bg = '#335267'

        player_col = sg.Column([
            [sg.Text('', size=(30, 1), font=("Helvetica", 14), key='output', background_color=player_col_bg)],
            [sg.ProgressBar(1000, orientation='h', size=(25, 10), key='progressbar', bar_color=("#fff", "#000"),
                            border_width=1)],
            [image_btn('Start', START_IMG), sg.Text(' ' * 2, background_color=player_col_bg),
             image_btn('Pause', PAUSE_IMG), sg.Text(' ' * 2, background_color=player_col_bg),
             image_btn('Stop', STOP_IMG), sg.Text(' ' * 4, background_color=player_col_bg),
             sg.Slider(range=(0, 10), default_value=5, size=(10, 10), orientation='horizontal', font=("Helvetica", 10),
                       background_color="#335267"),
             ],
        ], size=(320, 100), element_justification="left", vertical_alignment="top", background_color=player_col_bg)

        layout = [
            [sg.Text("Py Musical Text", text_color="#fff", font=("Roboto", 15, "bold"))],
            [input_text_col, file_name_col],
            [file_info_col, player_col],
            [sg.Exit(button_color='#dc3545')],
        ]

        return sg.Window(self.title, layout)
