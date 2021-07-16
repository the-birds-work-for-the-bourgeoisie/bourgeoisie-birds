from pathlib import Path, PosixPath
from typing import List


def get_files_in_folder_by_file_extension(folder: str, file_extension: str) -> List[PosixPath]:
    path_list = []
    path_list.extend(Path(folder).glob('**/*.' + file_extension.upper()))
    path_list.extend(Path(folder).glob('**/*.' + file_extension.lower()))
    return path_list
