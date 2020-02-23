class APIResourceMocks(object):

    def index(self):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        from foundations_core_rest_api_components.response import Response
        def _index():
            return 'some data'
        return Response('Mock', LazyResult(_index))

    class Mock(object):
        pass
        
    class MockWithIndex(object):
        def index(self):
            from foundations_core_rest_api_components.lazy_result import LazyResult
            from foundations_core_rest_api_components.response import Response
            def _index():
                return 'some data'
            return Response('Mock', LazyResult(_index))

    class MockWithPost(object):
        def post(self):
            from foundations_core_rest_api_components.lazy_result import LazyResult
            from foundations_core_rest_api_components.response import Response
            def _post():
                return 'some data'
            return Response('Mock', LazyResult(_post))

    class MockWithDelete(object):
        def delete(self):
            from foundations_core_rest_api_components.lazy_result import LazyResult
            from foundations_core_rest_api_components.response import Response
            def _delete():
                return 'some data'
            return Response('Mock', LazyResult(_delete))
    
    class MockWithPut(object):
        def put(self):
            from foundations_core_rest_api_components.lazy_result import LazyResult
            from foundations_core_rest_api_components.response import Response
            def _put():
                return 'some put data'
            return Response('Mock', LazyResult(_put))

    class ParamsMockWithPutAndStatus(object):
        status_code = -1

        def put(self):
            from foundations_core_rest_api_components.lazy_result import LazyResult
            from foundations_core_rest_api_components.response import Response
            def _put():
                return self.params
            return Response('Mock', LazyResult(_put), status=self.status_code)

    class MockWithDeleteAndStatus(object):
        def delete(self):
            from foundations_core_rest_api_components.lazy_result import LazyResult
            from foundations_core_rest_api_components.response import Response
            def _delete():
                return 'some data'
            return Response('Mock', LazyResult(_delete), status=403)

    class MockWithIndexAndPost(object):
        def index(self):
            from foundations_core_rest_api_components.lazy_result import LazyResult
            from foundations_core_rest_api_components.response import Response
            def _index():
                return 'some index data'
            return Response('Mock', LazyResult(_index))
            
        def post(self):
            from foundations_core_rest_api_components.lazy_result import LazyResult
            from foundations_core_rest_api_components.response import Response
            def _post():
                return 'some post data'
            return Response('Mock', LazyResult(_post))

    class ParamsMockWithIndex(object):
        def index(self):
            from foundations_core_rest_api_components.lazy_result import LazyResult
            from foundations_core_rest_api_components.response import Response
            def _index():
                return self.params
            return Response('Mock', LazyResult(_index))

    class ParamsMockWithPost(object):
        def post(self):
            from foundations_core_rest_api_components.lazy_result import LazyResult
            from foundations_core_rest_api_components.response import Response
            def _index():
                return self.params
            return Response('Mock', LazyResult(_index))

    class ParamsMockWithDelete(object):
        def delete(self):
            from foundations_core_rest_api_components.lazy_result import LazyResult
            from foundations_core_rest_api_components.response import Response
            def _delete():
                return self.params
            return Response('Mock', LazyResult(_delete))

    class ParamsMockWithIndexAndStatus(object):
        def index(self):
            from foundations_core_rest_api_components.lazy_result import LazyResult
            from foundations_core_rest_api_components.response import Response
            def _index():
                return self.params
            return Response('Mock', LazyResult(_index), status=403)

    class ParamsMockWithPostAndStatus(object):
        def post(self):
            from foundations_core_rest_api_components.lazy_result import LazyResult
            from foundations_core_rest_api_components.response import Response
            def _index():
                return self.params
            return Response('Mock', LazyResult(_index), status=403)

    class DifferentMockWithIndex(object):
        def index(self):
            from foundations_core_rest_api_components.lazy_result import LazyResult
            from foundations_core_rest_api_components.response import Response
            def _index():
                return 'some different data'
            return Response('Mock', LazyResult(_index))
