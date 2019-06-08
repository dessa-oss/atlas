"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

class _RestAPIServerProvider(object):

    _rest_api_server = None
    _queue = []

    class _APIPlaceHolder(object):

        def add_resource(self, resource_class, base_path):
            if _RestAPIServerProvider._rest_api_server is None:
                _RestAPIServerProvider._queue.append((resource_class, base_path))
            else:
                _RestAPIServerProvider._rest_api_server.api().add_resource(resource_class, base_path)

    def api(self):
        return self._APIPlaceHolder()

    @classmethod
    def reset(klass):
        klass._rest_api_server = None
        klass._queue = []

    @classmethod
    def store_rest_api_server(klass, rest_api_server):
        if klass._rest_api_server is None:
            klass._rest_api_server = rest_api_server
            klass._update_rest_api_server()

    @classmethod
    def get_rest_api_server(klass):
        return klass._rest_api_server

    @classmethod
    def _update_rest_api_server(klass):
        while len(klass._queue) > 0:
            resource_class, base_path = klass._queue.pop(0)
            klass._rest_api_server.api().add_resource(resource_class, base_path)


def register_rest_api_server(rest_api_server):
    _RestAPIServerProvider.store_rest_api_server(rest_api_server)


def get_rest_api_server():
    rest_api_server_reference = _RestAPIServerProvider.get_rest_api_server()
    if rest_api_server_reference is None:
        return _RestAPIServerProvider()
    return rest_api_server_reference
