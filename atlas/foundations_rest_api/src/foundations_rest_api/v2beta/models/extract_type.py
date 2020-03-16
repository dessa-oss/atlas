
from foundations_contrib.utils import is_string, is_number


def extract_type(value):
    if isinstance(value, bool):
        return "bool"

    if is_number(value):
        return "number"

    if is_string(value):
        return "string"

    if isinstance(value, list):
        return "array " + extract_type(value[0])

    return "unknown"
