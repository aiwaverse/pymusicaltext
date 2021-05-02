# %%
import PySimpleGUI as sg
from pymusicaltext.gui.layout import Layout
# %%
from pymusicaltext import Player


def main() -> None:
    layout = Layout("PyMusicalText")
    window = layout.make_gui()

    # TODO: remove dead code
    # progress = 0
    # progress_bar = window['progressbar']
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "Generate music":
            print(values)
            a_player = Player(values['in'], "file.mid")
            sg.popup('Musica Gerada com sucesso')

        # if progress < 1000:
        #     print(progress)
        #     progress += 10
        #     progress_bar.UpdateBar(progress)

        # if event == 'play':
        #     list_player.play()
        # if event == 'pause':
        #     list_player.pause()
        # if event == 'stop':
        #     list_player.stop()
        # if event == 'next':
        #     list_player.next()
        #     list_player.play()
        # if event == 'previous':
        #     list_player.previous()  # first call causes current video to start over
        #     list_player.previous()  # second call moves back 1 video from current
        #     list_player.play()
        # if event == 'load':
        #     if values['-VIDEO_LOCATION-'] and not 'Video URL' in values['-VIDEO_LOCATION-']:
        #         media_list.add_media(values['-VIDEO_LOCATION-'])
        #         list_player.set_media_list(media_list)
        #         window['-VIDEO_LOCATION-'].update('Video URL or Local Path:')  # only add a legit submit

        # update elapsed time if there is a video loaded and the player is playing
        # if player.is_playing():
        #     window['-MESSAGE_AREA-'].update(
        #         "{:02d}:{:02d} / {:02d}:{:02d}".format(*divmod(player.get_time() // 1000, 60),
        #                                                *divmod(player.get_length() // 1000, 60)))
        # else:
        #     window['-MESSAGE_AREA-'].update('Load media to start' if media_list.count() == 0 else 'Ready to play media')

    window.close()


if __name__ == "__main__":
    main()
# %%
