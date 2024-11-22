from os import listdir, path
from service.supported_types import SUPPORTED_TYPES


class FileManager:
    def __init__(self):
        self.folder_path = None

    def set_folder_path(self, folder_path: str) -> None:
        self.folder_path = folder_path

    def get_files(self) -> list[str]:
        return [file for file in listdir(self.folder_path) if file.endswith(SUPPORTED_TYPES)]

    def get_file_path(self, file_name) -> str:
        return path.join(self.folder_path, file_name)
