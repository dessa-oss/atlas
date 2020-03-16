
import os

def filter_pyc(directory_name, iterable):
    for file_name in iterable:
        if not file_name.endswith('.pyc'):
            yield os.path.join(directory_name, file_name)