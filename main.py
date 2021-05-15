# %%
from datetime import date, time
from pymusicaltext.gui.constants import VOLUME_CHANGE

import mido
import PySimpleGUI as sg

from pymusicaltext.gui.gui import GUI


def main() -> None:
    program_gui = GUI("PyMusicalText")
    while True:
        event, values = program_gui.read(timeout=1000)
        print(event)
        if event == "Gerar música" and not program_gui.empty_input():
            program_gui.create_player()
            sg.popup("Musica Gerada com sucesso")
            program_gui.make_full_gui_visible()
        if event == "Start":
            program_gui.start_song()
        if event == "Pause":
            program_gui.pause_song()
        if event == "Stop":
            program_gui.stop_song()
        if event == "Baixar":
            selected_folder = sg.popup_get_folder(
                "Por favor, entre com a pasta de destino",
                title="Baixar arquivo",
            )
            if selected_folder:
                program_gui.download_file(selected_folder)
        if event == VOLUME_CHANGE:
            program_gui.change_volume(values[VOLUME_CHANGE])
        if event == sg.WIN_CLOSED or event == "Exit":
            program_gui.close_player()
            break
        if program_gui.playing:
            program_gui.update_progress_bar()


# %%

if __name__ == "__main__":
    main()
