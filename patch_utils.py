from pathlib import Path
from dataclasses import dataclass

def add_in_file(filepath, search, replace):
    with open(filepath, 'r', encoding="utf8") as file:
        data = file.read()
        if search not in data:
            raise LookupError(f"File {filepath}: string {search} not found")
        if replace not in data:
            data = data.replace(search, replace)
        else:
            raise LookupError(f"File {filepath} already contains the patch {replace}")

    with open(filepath, 'w', encoding="utf8") as file:
        file.write(data)

def replace_in_file(filepath, search, replace):
    with open(filepath, 'r', encoding="utf8") as file:
        data = file.read()
        if search not in data:
            raise LookupError(f"File {filepath}: string {search} not found")
        data = data.replace(search, replace)

    with open(filepath, 'w', encoding="utf8") as file:
        file.write(data)


@dataclass
class Addition:
    filepath: Path
    search: str
    add: str