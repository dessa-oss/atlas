"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def l_infinity(reference_percentages, current_percentages):
    import numpy

    if len(reference_percentages) == 0:
        raise ValueError('cannot take l_infinity distance of empty arrays')
    
    absolute_difference = numpy.abs(reference_percentages - current_percentages)
    return numpy.max(absolute_difference)

def bin_values(*args):
    pass