"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.utils.api_resource import api_resource
from flask import request


@api_resource('/api/v1/login')
class SessionController(object):

    def post(self):
        from foundations_rest_api.response import Response
        from foundations_rest_api.lazy_result import LazyResult

        print(request.form.get('password'))


        def _random_lazy_result():
            return 'Bad request'

        return Response('Session', LazyResult(_random_lazy_result), status=400)
