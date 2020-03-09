
def is_string(string):
    return isinstance(string, str)

def string_from_bytes(string):
    if is_string(string):
        return string
    else:
        return string.decode()

