"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 12 2018
"""


class BoolParser(object):

    def parse(self, value):
        return True if self._is_true(value) else False if self._is_false(value) else None

    def _is_true(self, value):
        return str(value).title() == 'True'

    def _is_false(self, value):
        return str(value).title() == 'False'
