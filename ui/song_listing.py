from tkinter import *
from tkinter import font
from typing import Callable
from service.supported_types import SUPPORTED_TYPES


class SongListing:
    def __init__(self, master: Widget, file_name: str, row_num: int, play_song: Callable,
                 song_changed_event: list[Callable]):

        self.file_name = file_name
        self.default_label_fg = '#757575'

        self.label_font = font.Font(size=10)

        self.label = Label(master, text=self.get_label_text(), fg=self.default_label_fg, font=self.label_font)
        self.button = Button(master, text='>', command=lambda: play_song(file_name))

        self.label.grid(row=row_num, column=0, pady=3)
        self.button.grid(row=row_num, column=1)

        self.song_changed_event = song_changed_event
        song_changed_event.append(self.update_label_visual)

    def update_label_visual(self, current_song: str) -> None:
        if self.file_name == current_song:
            self.label.config(fg='green')
            self.label_font.config(underline=True)
        else:
            self.label.config(fg=self.default_label_fg)
            self.label_font.config(underline=False)

    def remove_listing(self) -> None:
        self.song_changed_event.remove(self.update_label_visual)
        self.label.destroy()
        self.button.destroy()

    def get_label_text(self) -> str:
        for suffix in SUPPORTED_TYPES:
            if self.file_name.endswith(suffix):
                return self.file_name[:-len(suffix)]

        return ''
