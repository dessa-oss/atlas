"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def quarantine(callback):
    if isinstance(callback, type):
        _warn(callback.__qualname__, is_class=True)

    class _raise_warning(object):

        def __init__(self):
            self.__name__ = callback.__name__
            self._qualname = callback.__qualname__

        def __call__(self, *args):
            _warn(self._qualname)

        @property
        def __unittest_skip__(self):
            _warn(self._qualname)
            return True
 
    return _raise_warning()

def _warn(test_name, is_class=False):
    import warnings

    if is_class:
        item_kind = 'TEST SUITE'
    else:
        item_kind = 'TEST'

    message = f'{item_kind} "{test_name}" IS QUARANTINED - PLEASE INVESTIGATE ASAP'
    hashes = '#' * len(message)
    warning = QuarantineWarning(f'\n{hashes}\n\n{message}\n\n{hashes}\n')
    warnings.warn(warning)

class QuarantineWarning(Warning):
    pass