
_WARNINGS = []

def quarantine(callback):
    import atexit

    global _WARNINGS

    if not _WARNINGS:
        atexit.register(_warning, _WARNINGS)

    _WARNINGS.append(callback.__qualname__)

    def _do_nothing(*args, **kwargs):
        pass

    _do_nothing.__unittest_skip__ = True
    _do_nothing.__name__ = callback.__name__
    return _do_nothing

def _warning(warning_list):
    import warnings

    message = _warning_message(warning_list)
    warnings.warn(QuarantineWarning(message))

def _warning_message(warning_list):
    warning_header = 'THE FOLLOWING ITEMS ARE QUARANTINED; PLEASE INVESTIGATE ASAP:'

    length_of_longest_message = max(map(len, [warning_header] + warning_list))

    hashes = '#' * length_of_longest_message

    message = f'\n{hashes}'
    message += f'\n\n{warning_header}\n'

    for warning_name in warning_list:
        message += f'\n{warning_name}'

    message += f'\n\n{hashes}\n'

    return message

class QuarantineWarning(Warning):
    pass