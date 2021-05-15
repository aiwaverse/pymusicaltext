"""
The main module of PyMusicalText, use it to run the
program as a graphical interactive interface
"""
import PySimpleGUI as sg

from pymusicaltext.gui.constants import (
    DOWNLOAD_BUTTON,
    EXIT,
    GENERATE_MUSIC,
    PAUSE,
    START,
    STOP,
    VOLUME_CHANGE,
)
from pymusicaltext.gui.interface import GUI


def main() -> None:
    """
    Main function
    """
    program_gui = GUI("PyMusicalText")
    while True:
        event, values = program_gui.read(timeout=1000)
        if event == GENERATE_MUSIC and not program_gui.empty_input():
            try:
                program_gui.create_player()
                sg.popup("Musica Gerada com sucesso")
                program_gui.make_full_gui_visible()
            except ValueError:
                continue
        if event == START:
            program_gui.start_song()
            program_gui.change_volume(values[VOLUME_CHANGE])
        if event == PAUSE:
            program_gui.pause_song()
        if event == STOP:
            program_gui.stop_song()
        if event == DOWNLOAD_BUTTON:
            selected_folder = sg.popup_get_folder(
                "Por favor, entre com a pasta de destino",
                title="Baixar arquivo",
            )
            if selected_folder:
                program_gui.download_file(selected_folder)
        if event == VOLUME_CHANGE:
            program_gui.change_volume(values[VOLUME_CHANGE])
        if event in (sg.WIN_CLOSED, EXIT):
            program_gui.close_player()
            break
        if program_gui.playing:
            program_gui.update_progress_bar()


if __name__ == "__main__":
    main()
