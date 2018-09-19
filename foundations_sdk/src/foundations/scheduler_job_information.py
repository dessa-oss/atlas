"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

class JobInformation(object):
    def __init__(self, uuid, submission_timestamp, duration_timestamp, status, user_submitted):
        self._uuid = uuid
        self._submission_timestamp = submission_timestamp
        self._duration_timestamp = duration_timestamp
        self._status = status
        self._user = user_submitted

    def submission_datetime(self):
        from datetime import datetime
        return datetime.utcfromtimestamp(self._submission_timestamp)

    def status(self):
        return self._status

    def uuid(self):
        return self._uuid

    def user_submitted(self):
        return self._user
    
    def duration(self):
        return self._duration_timestamp