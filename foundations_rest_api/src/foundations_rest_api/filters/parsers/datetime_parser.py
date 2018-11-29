"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
from datetime import datetime

class DateTimeParser(object):

    def parse(self, value):
        if isinstance(value, datetime):
            return value
        return self._fromisoformat(value)

    def _fromisoformat(self, value):
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
