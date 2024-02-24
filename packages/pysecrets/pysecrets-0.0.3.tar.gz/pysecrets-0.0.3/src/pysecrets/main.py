import os
import sys
import re
import warnings
from typing import (List, Dict)

def load_secrets(alternate_name = '.secrets') -> None:
    file_path = __find_secrets_file(alternate_name)
    if not file_path:
        raise IOError('File not found')
    file_secrets = __read_secrets(file_path)
    for k,v in file_secrets.items():
        if k in os.environ:
            continue
        if v is not None:
            os.environ[k] = v


def __read_secrets(file_path: str) -> Dict[str, str]:
    secrets = {}
    with open(file_path, 'r') as f:
        for line_number, line in enumerate(f.readlines()):
            if re.match(r'^\s*#', line) or re.match(r'^\s*$', line):
                continue
            secret_search = re.search(r'([A-Z]+)=(.+$)', line)
            if secret_search:
                secrets[secret_search.group(1)] = secret_search.group(2)
            else:
                warnings.warn(f'Line {line_number+1} of .secrets file may not be formatted correctly.')
                print("EXAMPLE=p@ssword2")
    return secrets

def __paths_from_root(path: str) -> List[str]:
    if not os.path.exists(path):
        raise IOError('Path not found')

    if not os.path.isdir(path):
        path = os.path.dirname(path)

    current_directory = os.path.abspath(path)
    paths = [current_directory]
    while current_directory != '/':
        current_directory = os.path.abspath(os.path.join(os.path.abspath(current_directory), os.path.pardir))
        paths.append(current_directory)
    return paths

def __find_secrets_file(filename: str = '.secrets') -> str:
    path = os.path.dirname(os.path.abspath(filename))

    for directory in __paths_from_root(path):
        potential_path = os.path.join(directory, filename)
        if os.path.isfile(potential_path):
            return potential_path
    return ''
