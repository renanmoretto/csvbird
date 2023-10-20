'''

Attributes and properties:
    .path
    .delimiter
    .fieldnames

Methods:
    .insert(data: list | dict)
    .filter_by(**kw)
    .delete(**kw)
    .delete_field(fieldname: str | list[str])
    .change_delimiter(new_delimiter: str)
    .copy()
    .len()
    .nrows()
    .nfields()
    .to_dict()
    .to_json()
    .to_list()

Constructors/classmethods:
    .new()

'''


import csv
import json

from pathlib import Path
from typing import Iterable
from io import TextIOWrapper

class CSVBird():
    def __init__(
        self, 
        file_path: str | Path,
        delimiter: str = ',',
        fieldnames: list[str] | None = None,
        fieldvalues: list | None = None,
        # types: dict | None = None,        # Not implemented
    ):
        path = _ensure_path(file_path)

        if not path.exists():
            if fieldnames is None:
                raise ValueError("Please pass 'fieldnames' if ")
            _create_new_file(path)

        # Set attrs
        self.path = path
        self.delimiter = delimiter

    @property
    def empty(self):
        with open(self.path, 'r') as f:
            lines = f.readlines()
            if lines:
                return False
            return True

    @property
    def fieldnames(self) -> list[str]:
        with open(self.path, 'r') as f:
            fieldnames = csv.DictReader(f).fieldnames
            if fieldnames:
                return list(fieldnames)
            else:
                return []
            
    def __len__(self):
        with open(self.path, 'r') as f:
            return sum(1 for _ in f)
        
    # Main methods
    def insert(self, data: dict):
        path = self.path
        delimiter = self.delimiter
        fieldnames = self.fieldnames
        empty = self.empty

        file_header = _get_file_header(path)
        if file_header != fieldnames:
            new_header = f'{delimiter}'.join(fieldnames)
            _change_file_header(path, new_header)

        with open(path, 'a', newline='') as f:
            writer = csv.DictWriter(f, delimiter=delimiter, fieldnames=fieldnames)
            if empty:
                writer.writeheader()
            writer.writerow(data)
            

    #TODO
    '''
    def to_dict(self,) -> dict: pass
    def to_json(self,) -> json: pass
    '''

# ----------------------------------- utils ---------------------------------- #

def _ensure_path(path: str | Path) -> Path:
    if isinstance(path, str):
        return Path(path)
    elif isinstance(path, Path):
        return path
    else:
        raise TypeError(f'path must be str or Path')

def _create_new_file(path: Path):
    with open(path, 'w') as _:
        pass

def _get_file_header(path: Path) -> str:
    with open(path, 'r') as file:
        header = file.readline().replace('\n','')
    return header

def _change_file_header(path: Path, new_header: str) -> None:
    with open(path, 'r') as file:
        file.readline()
        remaining_lines = file.read()

    with open(path, 'w') as file:
        file.write(f'{new_header}\n')
        file.write(remaining_lines)