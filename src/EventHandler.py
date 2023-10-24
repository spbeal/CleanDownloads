import shutil
from datetime import date
from pathlib import Path

from watchdog.events import FileSystemEventHandler

from extensions import extension_paths


def add_date_to_path(path: Path):
    """
    Adds current year/month to destination path. 
    If the path doesn't already exist, it is created.

    / f'{date.today().month:02d}
    """
    dated_path = path / f'{date.today().year}' 
    dated_path.mkdir(parents=True, exist_ok=True)
    return dated_path


def rename_file(source: Path, destination_path: Path):
    """
    Renames file to reflect new path. If a file of the same
    name already exists in the destination folder, the file name is numnered and
    incremented until the filename is unique
    """
    if Path(destination_path / source.name).exists():
        increment = 0

        while True:
            increment += 1
            new_name = destination_path / f'{source.stem}_{increment}{source.suffix}'

            if not new_name.exists():
                return new_name
    else:
        return destination_path / source.name

class EventHandler(FileSystemEventHandler):
    def __init__(self, watch_path: Path, destination_root: Path):
        self.watch_path = watch_path.resolve()
        self.destination_root = destination_root.resolve()

    def on_modified(self, event):
        for child in self.watch_path.iterdir(): # Can change watch path to whatever
            # skips directories and non-specified extensions
            if child.is_file() and child.suffix.lower() in extension_paths:
                #destination_path = self.destination_root / extension_paths[child.suffix.lower()]
                #destination_path = add_date_to_path(path=destination_path)
                destination_path = self.destination_root  # uncomment to complete base case or move to specified areas
                destination_path = rename_file(source=child, destination_path=destination_path) # accounts for duplicates
                shutil.move(src=child, dst=destination_path)