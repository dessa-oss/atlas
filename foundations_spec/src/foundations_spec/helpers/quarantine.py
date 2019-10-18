"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def quarantine(callback):

    class _raise_warning(object):

        def __init__(self):
            self.__name__ = callback.__name__

        def __call__(self, *args):
            pass

        @property
        def __unittest_skip__(self):
            import warnings
            warning = QuarantineWarning('------ test is quarantined - please investigate asap')
            warnings.warn(warning)

            return True

    return _raise_warning()

class QuarantineWarning(Warning):
    pass