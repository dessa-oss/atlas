
from foundations_core_rest_api_components.v1.controllers.authentication_controller import AuthenticationController

from foundations_core_rest_api_components.global_state import app_manager
app_manager.api().add_resource(AuthenticationController, "/api/v2beta/auth/<string:action>")