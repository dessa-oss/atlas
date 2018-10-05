"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from sys import version_info

def file_archive_name(prefix, name):
    if prefix is not None:
        return prefix + '/' + name
    else:
        return name


def file_archive_name_with_additional_prefix(prefix, additional_prefix, name):
    return file_archive_name(prefix, additional_prefix + '/' + name)

if version_info[0] < 3:
    def force_encoding(string):
        return string.decode('utf-8').encode('utf-8', 'ignore')

    def is_string(string):
        return isinstance(string, basestring)
else:
    def force_encoding(string):
        return string.encode('utf-8', 'ignore')

    def is_string(string):
        return isinstance(string, str)

def byte_string(string):
    if isinstance(string, bytes):
        return string
    else:
        return bytes(force_encoding(string))

def string_from_bytes(string):
    if is_string(string):
        return string
    else:
        return string.decode()
  
def generate_uuid(string):
    from hashlib import sha1
    digest = sha1()
    encoded_string = force_encoding(string)
    digest.update(encoded_string)
    return digest.hexdigest()


def merged_uuids(uuids):
    from hashlib import sha1
    digest = sha1()
    for uuid in uuids:
        encoded_string = force_encoding(uuid)
        digest.update(encoded_string)
    return digest.hexdigest()

def make_uuid(item, iterable_callback):
    if isinstance(item, list):
        return merged_uuids([iterable_callback(sub_item) for sub_item in item])

    if is_string(item):
        return generate_uuid(item)

    return generate_uuid(str(item))

def tgz_archive_without_extension(archive_path):
    return archive_path[0:-4]

def _list_items(arr):
    for i in range(len(arr)):
        yield i, arr[i]

def dict_like_iter(dict_like):
    from collections import Iterable

    if isinstance(dict_like, dict):
        return dict_like.items()

    if isinstance(dict_like, Iterable):
        return _list_items(dict_like)

    return []
    
def dict_like_append(dict_like, key, val):
    from collections import Iterable
        
    if isinstance(dict_like, dict):
        dict_like[key] = val
    elif isinstance(dict_like, Iterable):
        dict_like.append(val)

def pretty_time(timestamp):
    import datetime

    try:
        return datetime.datetime.fromtimestamp(timestamp)
    except:
        return timestamp

def restructure_headers(all_headers, first_headers):
    def diff(list_0, list_1):
        set_1 = set(list_1)
        return [item for item in list_0 if item not in set_1]

    def intersect(list_0, list_1):
        set_1 = set(list_1)
        return [item for item in list_0 if item in set_1]

    return intersect(first_headers, all_headers) + diff(all_headers, first_headers)

def concat_strings(iterable):
    return "".join(iterable)

def pretty_error(pipeline_name, error_info):
    import traceback

    from foundations.error_printer import ErrorPrinter

    if error_info is None:
        return None

    error_name = ["\n", error_info["type"].__name__, ": ", str(error_info["exception"]), "\n"]
    traceback_items = error_info["traceback"]

    error_printer = ErrorPrinter()
    filtered_traceback = error_printer.transform_extracted_traceback(traceback_items)
    filtered_traceback_strings = traceback.format_list(filtered_traceback)

    error_message = concat_strings(error_name + filtered_traceback_strings).rstrip("\n")

    return error_message, error_printer.get_callback()

def split_process_output(output):
    lines = output.decode().strip().split("\n")
    lines = filter(lambda line: len(line) > 0, lines)
    return lines

def take_from_generator(elems_to_take, generator):
    for _ in range(elems_to_take):
        try:
            yield next(generator)
        except StopIteration:
            return

def _remove_items_by_key(dictionary, keys):
    for key in keys:
        dictionary.pop(key)

def directory_path(path, name):
    from os.path import dirname
    from os.path import join

    return join(path, dirname(name))

def ensure_path_exists(path, name):
    from distutils.dir_util import mkpath
    from os.path import isdir

    directory = directory_path(path, name)
    _log().debug('Ensuring that {} exists'.format(directory))
    if not isdir(directory):
        _log().debug('Creating {}'.format(directory))
        result = mkpath(directory)
        _log().debug('{} created'.format(result))
    else:
        _log().debug('{} Already exists'.format(directory))

def _log():
    from foundations.global_state import log_manager
    return log_manager.get_logger(__name__)

def split_at(list_of_results, slot_index):
    return list_of_results[slot_index]

def whoami():
    """Get the currently logged-in user.

    Returns:
        user_name -- The name of the currently logged-in user as a string.
    """

    import os

    # if LOGNAME is not set but user is, using ".get()" will fail
    return os.environ["USER"] if "USER" in os.environ else os.environ["LOGNAME"]

def get_foundations_root():
    """Return the directory containing the foundations module's init py.

    Returns:
        dir_path -- As above
    """

    import sys
    from os.path import dirname

    return dirname(sys.modules["foundations"].__file__)

def check_is_in_dir(parent_directory, child_file):
    """Check to see whether a filepath could in principle exist in a directory.  Does not check whether the file nor directory exists - just checks to see whether the names are plausible.
        Arguments:
            parent_directory: {str} -- The absolute path of a candidate parent directory.
            child_file: {str} -- The absolute filepath of a candidate child file

    Returns:
        bool -- Whether child_file could be in parent_directory (in principle).
    """

    from os.path import dirname

    child_directory = dirname(child_file)
    return child_directory.startswith(parent_directory)

def datetime_string(time):
    from datetime import datetime

    if time is None:
        return 'No time available'
    date_time = datetime.fromtimestamp(time)
    return date_time.isoformat()
    