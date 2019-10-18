"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def quarantine(callback):
    import atexit

    atexit.register(_warning, callback.__qualname__, is_class=isinstance(callback, type))

    def _do_nothing(*args, **kwargs):
        pass

    _do_nothing.__unittest_skip__ = True
    _do_nothing.__name__ = callback.__name__
    return _do_nothing

def _warning(name, is_class):
    import warnings

    if is_class:
        item_type = 'TEST SUITE'
    else:
        item_type = 'TEST'

    message = f'{item_type} "{name}" IS QUARANTINED - PLEASE INVESTIGATE ASAP'
    hashes = '#' * len(message)

    full_message = f'\n{hashes}\n\n{message}\n\n{hashes}\n'
    warnings.warn(QuarantineWarning(full_message))

class QuarantineWarning(Warning):
    pass