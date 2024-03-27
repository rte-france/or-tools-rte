from pathlib import Path
from dataclasses import dataclass

def replace_in_file(filepath, search, replace):
    with open(filepath, 'r', encoding="utf8") as file:
        data = file.read()
        data = data.replace(search, replace)

    with open(filepath, 'w', encoding="utf8") as file:
        file.write(data)


@dataclass
class Addition:
    filepath: Path
    search: str
    add: str