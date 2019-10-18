"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def quarantine(callback):
    def _raise_warning(self):
        import warnings
        warning = QuarantineWarning('------ test is quarantined - please investigate asap')
        warnings.warn(warning)

    _raise_warning.__name__ = callback.__name__
    return _raise_warning

class QuarantineWarning(Warning):
    pass