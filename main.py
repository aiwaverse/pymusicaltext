#%%
from pymusicaltext import Player
import PySimpleGUI as sg


def make_gui(title: str) -> sg.Window:
        layout = [
            [sg.Multiline(write_only=True, size=(50,20), default_text="Decoded song goes here...", key='-OUT-')],
            [sg.Text("Enter the text:")],
            [sg.Multiline(size=(50,14), focus=True, key='-IN-')],
            [sg.Button("Generate music"), sg.Exit()],
        ]
        return sg.Window(title, layout)

def main() -> None:
    gui = make_gui("PyMusicalText")
    #a_player = Player("aaaaaaaaaaa", "file.mid")
    while True:
        event, values = gui.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == "Generate music":
            gui["-OUT-"].update(values["-IN-"])
    gui.close()


if __name__ == "__main__":
    main()
# %%
