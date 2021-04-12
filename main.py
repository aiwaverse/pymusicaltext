# %%
import PySimpleGUI as sg


# %%


def make_gui(title: str) -> sg.Window:
    sg.theme('DarkBlack1')

    layout = [
        [sg.Text("Convert Text <-> Music", text_color="#fff", font=("Roboto", 15, "bold"))],
        [sg.Text("Type a text:", text_color="#fff", font=("Roboto", 11, "bold"))],
        [
            sg.Multiline(
                write_only=True,
                font=("Ubuntu", 11),
                size=(40, 10),
                default_text="Decoded song goes here...",
                key="-IN-",
                focus=True,
            ),
            sg.Button("Generate music", button_color='#8257e6', border_width=0, font=("Ubuntu", 11), size=(20, 1))
        ],
        [sg.Text("Or choose a file:", text_color="#fff", font=("Roboto", 11, "bold"))],
        [sg.Input(size=(30, 20), font=("Ubuntu", 11)),
         sg.FileBrowse(button_color='#8257e6', font=("Ubuntu", 11))],
        [sg.Button("Generate music", button_color='#8257e6', border_width=0, font=("Ubuntu", 11), size=(20, 1))],
        [sg.Exit(button_color='#dc3545')],
    ]
    return sg.Window(title, layout)


def main() -> None:
    gui = make_gui("PyMusicalText")
    # a_player = Player("aaaaaaaaaaa", "file.mid", )
    while True:
        event, values = gui.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "Generate music":
            gui["-OUT-"].update(values["-IN-"])
    gui.close()


if __name__ == "__main__":
    main()
# %%
