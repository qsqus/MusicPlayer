import pygame
from pygame import mixer
from random import choice
from data.file_manager import FileManager
from tkinter import Tk


class Player:
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager

        self.song_list = []

        self.current_track_idx = None
        self.track_history = []
        self.is_random = False

        self.song_changed_event = []

        mixer.init()
        pygame.init()

        self.MUSIC_END_EVENT = pygame.USEREVENT + 1
        mixer.music.set_endevent(self.MUSIC_END_EVENT)

    def play(self, song_name: str, add_to_history: bool = True) -> None:
        if not self.has_songs():
            return

        for listener in self.song_changed_event:
            listener(song_name)

        for i, file in enumerate(self.song_list):
            if file == song_name:
                self.current_track_idx = i
                if add_to_history:
                    self.track_history.append(self.current_track_idx)
                mixer.music.load(self.file_manager.get_file_path(file))
                mixer.music.play()
                break

    def play_random(self) -> None:
        if not self.has_songs():
            return

        available_files = [file for i, file in enumerate(self.song_list) if i != self.current_track_idx]
        self.play(choice(available_files))

    def toggle_random(self) -> None:
        self.is_random = not self.is_random
        if self.is_random:
            self.play_random()

    def toggle_pause(self) -> None:
        if not self.has_songs():
            return

        if mixer.music.get_busy():
            mixer.music.pause()
        else:
            mixer.music.unpause()

    def replay(self) -> None:
        if not self.has_songs():
            return

        self.play(self.song_list[self.current_track_idx], False)

    def play_next(self) -> None:
        if not self.has_songs():
            return

        if self.is_random:
            self.play_random()
        else:
            self.current_track_idx += 1
            self.current_track_idx = 0 if self.current_track_idx >= len(self.song_list) else self.current_track_idx
            next_song = self.song_list[self.current_track_idx]

            self.play(next_song)

    def play_previous(self) -> None:
        if not self.has_songs():
            return

        if len(self.track_history) > 1:
            self.track_history.pop()
            previous_song = self.song_list[self.track_history[-1]]
            self.track_history.pop()
        else:
            previous_song_idx = self.current_track_idx - 1
            previous_song_idx = 0 if previous_song_idx < 0 else previous_song_idx
            previous_song = self.song_list[previous_song_idx]

        self.play(previous_song, False)

    def check_song_finished(self, root: Tk) -> None:
        if self.has_songs():
            for event in pygame.event.get():
                if event.type == self.MUSIC_END_EVENT:
                    self.play_next()

            root.after(50, lambda: self.check_song_finished(root))

    def update_song_list(self) -> None:
        self.current_track_idx = 0
        self.track_history = []
        mixer.music.stop()

        self.song_list = self.file_manager.get_files()

    def has_songs(self) -> bool:
        return len(self.song_list) != 0 and self.current_track_idx is not None
