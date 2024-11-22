from tkinter import *
from tkinter import filedialog, ttk, messagebox
from ui.song_listing import SongListing
from typing import Callable
from service.player import Player
from data.file_manager import FileManager
from os import path


class UserInterface:
    def __init__(self, root: Tk, window_name: str, player: Player, file_manager: FileManager):
        root.title(window_name)

        self.main_frame = Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        folder_settings = Frame(self.main_frame)
        folder_settings.pack(pady=(0, 10))

        folder_button = Button(folder_settings, text='Open folder', command=lambda: self.open_folder(file_manager,
                                                                                                     player))
        self.folder_name = Label(folder_settings)

        folder_button.grid(row=0, column=0)
        self.folder_name.grid(row=0, column=1)

        self.add_separator()

        self.song_listings = []
        self.song_list = Frame(self.main_frame)
        self.song_list.pack()

        self.add_separator()

        button_frame = Frame(self.main_frame)
        button_frame.pack()

        previous_button = Button(button_frame, text='<<', command=player.play_previous)
        self.pause_button = Button(button_frame, text='Toggle pause', width=20, command=player.toggle_pause)
        next_button = Button(button_frame, text='>>', command=player.play_next)
        replay_button = Button(button_frame, text='Replay', width=10, command=player.replay)
        random_check = Checkbutton(button_frame, text='Play random', command=player.toggle_random)

        random_check.grid(row=0, column=0, columnspan=3)
        previous_button.grid(row=1, column=0, rowspan=2)
        self.pause_button.grid(row=1, column=1, padx=5, pady=5)
        next_button.grid(row=1, column=2, rowspan=2)
        replay_button.grid(row=2, column=1)

    def list_songs(self, song_names: list[str], play: Callable, song_changed_event: list[Callable]) -> None:
        self.song_listings = []
        for i, s in enumerate(song_names):
            sl = SongListing(self.song_list, s, i, play, song_changed_event)
            self.song_listings.append(sl)

    def open_folder(self, file_manager: FileManager, player: Player) -> None:
        folder_path = filedialog.askdirectory(title="Select a Folder")

        if not path.exists(folder_path):
            messagebox.showerror('Error', f'Selected folder doesn\'t exist!' )
            return

        file_manager.set_folder_path(folder_path)

        self.folder_name.config(text=path.basename(folder_path))
        self.clear_song_list()
        self.list_songs(file_manager.get_files(), player.play, player.song_changed_event)
        player.update_song_list()

    def clear_song_list(self) -> None:
        for s in self.song_listings:
            s.remove_listing()

    def add_separator(self) -> None:
        separator = ttk.Separator(self.main_frame, orient='horizontal')
        separator.pack(fill='x', pady=3)
