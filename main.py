from ui.user_interface import UserInterface
from service.player import Player
from data.file_manager import FileManager
from tkinter import Tk


if __name__ == '__main__':
    root = Tk()

    file_manager = FileManager()
    player = Player(file_manager)
    ui = UserInterface(root, 'MusicPlayer', player, file_manager)

    player.check_song_finished(root)

    root.mainloop()
