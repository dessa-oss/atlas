

from foundations_contrib.utils import *
from foundations_internal.utils import *


def using_python_2():
    from sys import version_info
    return version_info[0] < 3


def byte_string(string):
    if isinstance(string, bytes):
        return string
    else:
        return bytes(force_encoding(string))



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

    if error_info is None:
        return None

    error_name = ["\n", error_info["type"].__name__,
                  ": ", str(error_info["exception"]), "\n"]
    traceback_items = error_info["traceback"]

    filtered_traceback_strings = traceback.format_list(traceback_items)

    error_message = concat_strings(error_name + filtered_traceback_strings).rstrip("\n")

    return error_message, generate_compatible_error_callback()

    def generate_compatible_error_callback():
        def _callback(ex_type, ex_value, ex_traceback):
            """
            Arguments:
                ex_type: {type} -- The type of the exception to which the stack trace belongs.
                ex_value: {Exception} -- The exception value itself.
                ex_traceback: {TracebackType} -- The traceback for the exception.
            """
            error_msg = f'Type: {ex_type}, Value: {ex_value}, Traceback: {ex_traceback}'
            self._log().error(error_msg)
            
        return _callback

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
    import os

    directory = directory_path(path, name)
    _log().debug('Ensuring that {} exists'.format(directory))
    os.makedirs(directory, exist_ok=True)


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


def log_warning_if_not_running_in_job(function_if_running_in_job, *args):
    from foundations_contrib.global_state import log_manager, current_foundations_job

    if current_foundations_job().is_in_running_job():
        function_if_running_in_job(*args)
    elif not log_manager.foundations_not_running_warning_printed():
        logger = log_manager.get_logger(__name__)
        logger.warning('Script not run with Foundations.')
        log_manager.set_foundations_not_running_warning_printed()

