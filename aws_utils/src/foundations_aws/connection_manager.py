"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""


class ConnectionManager(object):

    def __init__(self):
        self._bucket_connection = None

    def bucket_connection(self):
        if self._bucket_connection is None:
            self._load()

        return self._bucket_connection

    def _load(self):
        import boto3
        self._bucket_connection = boto.resource('s3')
