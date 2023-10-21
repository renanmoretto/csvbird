'''
This is the sole module of the csvbird library.
The library has no dependencies other than Python itself.

All the usage can be easily understood by this straightforward 
overview of the API:

Attributes and properties:
    .path
    .delimiter
    .fieldnames
    .nrows
    .nfields

Methods:
    .insert(data: dict)
    .filter_by(**kw)
    .delete(**kw)
    .delete_field(fieldname: str | list[str])
    .change_delimiter(new_delimiter: str)
    .copy()
    .len()
    .to_dict()
    .to_json()
    .to_list()
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
        # types: dict | None = None,        # Not implemented
    ):
        file_path = _ensure_path(file_path)

        if file_path.suffix != '.csv':
            raise ValueError('file_path suffix must be .csv')

        # Create new file if it doesn't exists
        if not file_path.exists():
            with open(file_path, 'w') as _:
                pass

        # Set attrs
        self.file_path = file_path
        self.delimiter = delimiter

        if (d:=_guess_file_delimiter(file_path)) != delimiter and not self.empty:
            print(f'WARNING: Looks like the csv delimiter is {d} and not {delimiter}')


    @property
    def empty(self):
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
            if lines:
                return False
            return True
    
    @property
    def fieldnames(self) -> list[str]:
        with open(self.file_path, 'r') as f:
            fieldnames = csv.DictReader(f).fieldnames
            if fieldnames:
                return fieldnames[0].split(self.delimiter)
            else:
                return []
            
    @property
    def nrows(self) -> int:
        return len(self)
    
    @property
    def nfields(self) -> int:
        return len(self.fieldnames)
    
    # __methods__
    def __len__(self):
        with open(self.file_path, 'r') as f:
            return sum(1 for _ in f)

    # .methods()
    def show(self, max_lines: int = 50):
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if i > max_lines:
                break
            adjusted_line = line.replace('\n','').replace(f'{self.delimiter}','\t')
            print(f'{adjusted_line}')

    def len(self):
        return len(self)
    
    def insert(self, data: dict):
        file_path = self.file_path
        delimiter = self.delimiter
        file_fieldnames = self.fieldnames
        data_fields = list(data.keys())

        if data_fields != file_fieldnames:
            new_fields = [field for field in data_fields if field not in file_fieldnames]
            new_fieldnames = file_fieldnames + new_fields
            new_header = f'{delimiter}'.join(new_fieldnames)
            _change_file_header(file_path, new_header)
            fieldnames = new_header.split(delimiter)
        else:
            fieldnames = file_fieldnames

        with open(file_path, 'a', newline='') as f:
            writer = csv.DictWriter(f, delimiter=delimiter, fieldnames=fieldnames)
            writer.writerow(data)

    #TODO 's
    def add(self, bird: 'CSVBird'): ...
    def filter_by(self): ...
    def delete(self): ...
    def delete_field(self): ...
    def change_delimiter(self): ...
    def copy(self): ...
    def to_dict(self): ...
    def to_json(self): ...
    def to_lists(self): ...     # ?

# ----------------------------------- utils ---------------------------------- #

def _ensure_path(path: str | Path) -> Path:
    if isinstance(path, str):
        return Path(path)
    elif isinstance(path, Path):
        return path
    else:
        raise TypeError(f'path must be str or Path')

def _guess_file_delimiter(file_path):
    with open(file_path, 'r') as f:
        first_line = f.readline()
    possible_delimiters = [',', ';', '\t', '|', ':']
    delimiter = max(possible_delimiters, key=first_line.count)
    return delimiter

def _get_file_header(file_path: Path) -> str:
    with open(file_path, 'r') as file:
        header = file.readline().replace('\n','')
    return header

def _change_file_header(file_path: Path, new_header: str) -> None:
    with open(file_path, 'r') as file:
        file.readline()
        remaining_lines = file.read()

    with open(file_path, 'w') as file:
        file.write(f'{new_header}\n')
        file.write(remaining_lines)