# %%
from pymusicaltext import Player
from pymusicaltext.gui.layout import Layout
import PySimpleGUI as sg
import mido
import pymusicaltext.gui.constants as gui_constants
from datetime import date

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

            player = Player(values[gui_constants.IN_TEXT_INPUT], values[gui_constants.IN_FILE_NAME], port)
            player.generate_notes()
            file = player.generate_file()

            window[gui_constants.TEXT_FILE_NAME].update(values[gui_constants.IN_FILE_NAME])
            window[gui_constants.TEXT_DURATION].update(f"{file.length}s")
            window[gui_constants.TEXT_CREATED_AT].update(date.today().strftime("%d/%m/%Y"))

            sg.popup('Musica Gerada com sucesso')

        if event == 'Start':
            player.play_notes()

    window.close()
# %%

if __name__ == "__main__":
    main()
