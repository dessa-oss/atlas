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

    class MockWithShow(object):
        def show(self):
            from foundations_core_rest_api_components.lazy_result import LazyResult
            from foundations_core_rest_api_components.response import Response
            def _show():
                return 'some specific data'
            return Response('Mock', LazyResult(_show))

    class MockWithUpdate(object):
        def update(self):
            from foundations_core_rest_api_components.lazy_result import LazyResult
            from foundations_core_rest_api_components.response import Response
            def _update():
                return 'some updated data'
            return Response('Mock', LazyResult(_update))

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
