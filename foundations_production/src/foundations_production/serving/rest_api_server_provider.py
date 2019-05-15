"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

class _RestAPIServerProvider(object):

    _rest_api_server = None

    @classmethod
    def store_rest_api_server(klass, rest_api_server):
        klass._rest_api_server = rest_api_server

    @classmethod
    def get_rest_api_server(klass):
        return klass._rest_api_server


def register_rest_api_server(rest_api_server):
    _RestAPIServerProvider.store_rest_api_server(rest_api_server)


def get_rest_api_server():
    rest_api_server_reference = _RestAPIServerProvider.get_rest_api_server()
    if rest_api_server_reference is None:
        return _RestAPIServerProvider()
    return rest_api_server_reference
