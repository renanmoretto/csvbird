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
        # types: dict | None = None,        # Not implemented
    ):
        file_path = _ensure_path(file_path)

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
    
    # __methods__
    def __len__(self):
        with open(self.file_path, 'r') as f:
            return sum(1 for _ in f)

    # .methods()
    def show(self):
        MAX_PRINT_LINES = 50         # Max print lines
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if i > MAX_PRINT_LINES:
                break
            adjusted_line = line.replace('\n','').replace(f'{self.delimiter}','\t')
            print(f'{adjusted_line}')

    def add(self, bird: 'CSVBird'):
        #TODO
        # self.insert(bird.to_dict())
        ...

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
            

    #TODO

# ----------------------------------- utils ---------------------------------- #

def _ensure_path(path: str | Path) -> Path:
    if isinstance(path, str):
        return Path(path)
    elif isinstance(path, Path):
        return path
    else:
        raise TypeError(f'path must be str or Path')

def _create_new_file(file_path: Path):
    with open(file_path, 'w') as _:
        pass

def _get_file_delimiter(file_path: Path) -> str:
    ...

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