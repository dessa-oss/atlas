"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class ConnectionManager(object):

    def __init__(self):
        pass

    def bucket_connection(self):
        from google.cloud.storage import Client
        return Client()       
