# %%
from pymusicaltext.core.constants import INSTRUMENT_MIN, VOLUME_DEFAULT
from pymusicaltext import Player, Generator, Parser
from pymusicaltext.core.midiinfo import AdvancedMidiInfo
import PySimpleGUI as sg
import mido

# %%

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
    string = "KJHEAJKHSDGAJHGSEJHAgsjHGAJYHGAIehjkASDHAoaiuweiawu3ee7891324y9j"
    p = Parser(string, tokens, True)
    decoded_input = p.parse()
    notes = [
        mido.MetaMessage("sequence_number", number=0, time=0),
        mido.MetaMessage("track_name", name="a_file", time=0),
    ]
    info = AdvancedMidiInfo(0, VOLUME_DEFAULT, 0, 120)
    for tok in decoded_input:
        partial_element = Generator(tok).generate()
        element = partial_element(info)
        notes += element.generate_message()
    i = 0
    for port in mido.get_output_names():
        print(f"{i} : {port}")
        i += 1
    option = int(input("Choose a port:"))
    port = str(mido.get_output_names()[option])
    print(port)
    file = mido.MidiFile()
    file.tracks.append(notes)
    with mido.open_output(name=port) as p:
        for msg in file.play():
            print(msg)
            p.send(msg)

# %%
