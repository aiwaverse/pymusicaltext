# %%
from datetime import date, time

import mido
import PySimpleGUI as sg

import pymusicaltext.gui.constants as gui_constants
from pymusicaltext import Player
from pymusicaltext.gui.layout import Layout

import os
import shutil

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
    playing = False
    time_unit = 0
    curr_fill = 0
    song_loaded = False
    while True:
        event, values = window.read(timeout=1000)
        if event == "Generate music":
            if (
                not values[gui_constants.IN_FILE_INPUT]
                and values[gui_constants.IN_TEXT_INPUT] == "\n"
            ):
                continue
            if not values[gui_constants.IN_FILE_NAME]:
                continue
            window[gui_constants.FILE_INFO_SECTION].update(visible=True)
            window[gui_constants.PLAYER_SECTION].update(visible=True)
            window["-SAVE-FILE-"].update(disabled=False)
            port = str(mido.get_output_names()[0])

            if values[gui_constants.IN_FILE_INPUT]:
                f = open(values[gui_constants.IN_FILE_INPUT], "r")
                input_string = f.read()
            else:
                input_string = values[gui_constants.IN_TEXT_INPUT]

            player = Player(
                input_string, values[gui_constants.IN_FILE_NAME], port
            )
            player.generate_notes()
            file = player.generate_file()
            time_unit = 100 / round(file.length)
            window[gui_constants.TEXT_FILE_NAME].update(
                values[gui_constants.IN_FILE_NAME]
            )
            window[gui_constants.TEXT_DURATION].update(f"{file.length}s")
            window[gui_constants.TEXT_CREATED_AT].update(
                date.today().strftime("%d/%m/%Y")
            )
            window["progressbar"].update(0)
            curr_fill = -time_unit

            sg.popup("Musica Gerada com sucesso")
        if event == "Start":
            if song_loaded:
                player.play_song()
            else:
                player.load_and_play_file(
                    f".tmp/{player.file_correct_name(file.filename)}.wav"
                )
                song_loaded = True
            playing = True

        if event == "Pause":
            playing = False
            player.pause_song()

        if event == "Stop":
            playing = False
            player.stop_song()
            window["progressbar"].update(0)
            curr_fill = -time_unit

        # não feito
        if event == "-SAVE-FILE-":
            print("Atingido")
            target = values["-SAVE-FILE-"]
            print(target)
            #shutil.copy(
            #    f".tmp/{player.file_correct_name(file.filename)}.mid", target
            #)

        if event == sg.WIN_CLOSED or event == "Exit":
            os.remove(f".tmp/{file.filename}.wav")
            os.remove(f".tmp/{file.filename}.mid")
            break

        if playing:
            window["progressbar"].update(time_unit + curr_fill)
            curr_fill += time_unit

    window.close()


# %%

if __name__ == "__main__":
    main()
