from pathlib import Path
from dataclasses import dataclass

def add_in_file(filepath, search, replace):
    with open(filepath, 'r', encoding="utf8") as file:
        data = file.read()
        if search not in data:
            print(f"File {filepath}: string {search} not found, replace skipped")
            return
        if replace not in data:
            data = data.replace(search, replace)
        else:
            print(f"Skipping {filepath} as it already contains the patch {replace}")
            return

    with open(filepath, 'w', encoding="utf8") as file:
        file.write(data)

def replace_in_file(filepath, search, replace):
    with open(filepath, 'r', encoding="utf8") as file:
        data = file.read()
        if search not in data:
            print(f"File {filepath}: string {search} not found, replace skipped")
            return
        data = data.replace(search, replace)

    with open(filepath, 'w', encoding="utf8") as file:
        file.write(data)


@dataclass
class Addition:
    filepath: Path
    search: str
    add: str