from foundations_rest_api.utils.api_resource import api_resource

from foundations_core_rest_api_components.v1.controllers.authentication_controller import AuthenticationController

AuthenticationController = api_resource('/api/v2beta/auth/<string:action>')(AuthenticationController)