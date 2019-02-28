"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ConnectionManager(object):

    def __init__(self):
        self._bucket_connection = None

    def bucket_connection(self):
        from google.cloud.storage import Client      
        from foundations_gcp.authorized_storage_session import AuthorizedStorageSession

        if not self._bucket_connection:
            _http = AuthorizedStorageSession(
                pool_size=30,
                pool_block=True,
                max_retries=3,
            )
            self._bucket_connection = Client(_http=_http)
            
        return self._bucket_connection


