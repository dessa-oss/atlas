
import os

from lib.utils.filtering import filter_pyc

def all_files():
    for directory_name, _, files in os.walk('.'):
        yield from filter_pyc(directory_name, files)