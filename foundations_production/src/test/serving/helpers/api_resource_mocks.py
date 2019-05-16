"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
class APIResourceMocks(object):

    def get(self):
        from foundations_rest_api.lazy_result import LazyResult
        from foundations_rest_api.response import Response
        def _index():
            return 'some data'
        return Response('Mock', LazyResult(_index))

    class Mock(object):
        pass

    class MockWithIndex(object):
        def get(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _index():
                return 'some data'
            return Response('Mock', LazyResult(_index))

    class MockWithPost(object):
        def post(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _post():
                return 'some data'
            return Response('Mock', LazyResult(_post))

    class MockWithIndexAndPost(object):
        def get(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _index():
                return 'some index data'
            return Response('Mock', LazyResult(_index))

        def post(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _post():
                return 'some post data'
            return Response('Mock', LazyResult(_post))

    class ParamsMockWithIndex(object):
        def get(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _index():
                return self.params
            return Response('Mock', LazyResult(_index))

    class ParamsMockWithIndexAndStatus(object):
        def get(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _index():
                return self.params
            return Response('Mock', LazyResult(_index), status=403)

    class ParamsMockWithPostAndStatus(object):
        def post(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _index():
                return self.params
            return Response('Mock', LazyResult(_index), status=403)

    class DifferentMockWithIndex(object):
        def get(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _index():
                return 'some different data'
            return Response('Mock', LazyResult(_index))

    class MockWithPut(object):
        def put(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _put():
                return 'some put data'
            return Response('Mock', LazyResult(_put))

    class ParamsMockWithPutAndStatus(object):
        status_code = -1

        def put(self):
            from foundations_rest_api.lazy_result import LazyResult
            from foundations_rest_api.response import Response
            def _put():
                return self.params
            return Response('Mock', LazyResult(_put), status=self.status_code)
