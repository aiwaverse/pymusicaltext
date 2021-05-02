# %%
import PySimpleGUI as sg

# %%
from pymusicaltext import Player
from pymusicaltext.gui.layout import Layout


def main() -> None:
    layout = Layout("PyMusicalText")
    window = layout.make_gui()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "Generate music":
            print(values)
            a_player = Player(values['in'], "file.mid")
            sg.popup('Musica Gerada com sucesso')

    window.close()


if __name__ == "__main__":
    main()
# %%
