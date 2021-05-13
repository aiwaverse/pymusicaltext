# %%
from datetime import date

import mido
import PySimpleGUI as sg

import pymusicaltext.gui.constants as gui_constants
from pymusicaltext import Player
from pymusicaltext.gui.layout import Layout

# %%

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


def main() -> None:
    layout = Layout("PyMusicalText")
    window = layout.make_gui()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "Generate music":
            window[gui_constants.FILE_INFO_SECTION].update(visible=True)
            window[gui_constants.PLAYER_SECTION].update(visible=True)

            port = str(mido.get_output_names()[0])

            if values[gui_constants.IN_FILE_INPUT]:
                f = open(values[gui_constants.IN_FILE_INPUT], "r")
                input_string = f.read()
            else:
                input_string = values[gui_constants.IN_TEXT_INPUT]

            player = Player(input_string, values[gui_constants.IN_FILE_NAME], port)
            player.generate_notes()
            file = player.generate_file()

            window[gui_constants.TEXT_FILE_NAME].update(values[gui_constants.IN_FILE_NAME])
            window[gui_constants.TEXT_DURATION].update(f"{file.length}s")
            window[gui_constants.TEXT_CREATED_AT].update(date.today().strftime("%d/%m/%Y"))

            sg.popup('Musica Gerada com sucesso')

        if event == 'Start':
            player.load_and_play_file(file.filename)

        if event == 'Pause':
            player.pause_song()

        if event == 'Stop':
            player.stop_song()

    window.close()


# %%

if __name__ == "__main__":
    main()
