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
        
        from foundations_gcp.authorized_storage_session import AuthorizedStorageSession

        authorized_session_kwargs = {
            "pool_size": 500,
            "pool_block": True,
            "max_retries": 3
        }

        _http = AuthorizedStorageSession(**authorized_session_kwargs)

        return Client(_http=_http)
