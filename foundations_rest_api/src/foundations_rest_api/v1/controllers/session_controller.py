"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.utils.api_resource import api_resource
from flask import request
import json
from http import HTTPStatus


@api_resource('/api/v1/login')
class SessionController(object):

    def post(self):      
        if 'password' in request.form:
            return self._authenticate_password()
        else:
            return self._response(HTTPStatus.BAD_REQUEST)

    def _response(self, error):
        from foundations_rest_api.lazy_result import LazyResult
        from foundations_rest_api.response import Response
        return Response('Session', LazyResult(lambda: error.phrase), status=error.value)
    
    def _authenticate_password(self):
        from foundations_rest_api.v1.models.session import Session
        password = request.form.get('password')
        if Session.auth(password) == 200:
            return self._response(HTTPStatus.OK)
        else:
            return self._response(HTTPStatus.UNAUTHORIZED)
        
