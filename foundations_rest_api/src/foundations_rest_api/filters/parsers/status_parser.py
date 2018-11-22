"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

class StatusParser(object):

    _valid_statuses = ['QUEUED', 'RUNNING', 'COMPLETED', 'FAILED']

    def parse(self, value):
        if not (isinstance(value, str) and value.upper() in self._valid_statuses):
            return None
        return value.upper()
