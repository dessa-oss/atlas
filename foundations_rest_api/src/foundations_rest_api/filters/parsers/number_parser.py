"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 12 2018
"""


class NumberParser(object):

    def parse(self, value):
        try:
            return float(value)
        except TypeError:
            raise ValueError('Not able to convert "{}" to a number'.format(str(value)))
