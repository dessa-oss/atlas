"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

class ControllerMixin(object):

    def _get_model_id_from_model_package_mapping(self):
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server
        from foundations_production.exceptions import MissingModelPackageException

        rest_api_server = get_rest_api_server()
        model_package_mapping = rest_api_server.get_model_package_mapping()
        user_defined_model_name = self.params['user_defined_model_name']
        if user_defined_model_name in model_package_mapping:
            return model_package_mapping[user_defined_model_name]
        else:
            raise MissingModelPackageException(user_defined_model_name)
