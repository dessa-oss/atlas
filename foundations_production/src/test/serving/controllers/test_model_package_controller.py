"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from foundations_spec import *
from mock import patch

class TestModelPackageController(Spec):

    package_pool_mock = Mock()
    mock_job = let_mock()
    communicator = let_mock()

    @let
    def model_package_id(self):
        return self.faker.uuid4()
    
    @let
    def user_defined_model_name(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        from foundations_production.serving.controllers.model_package_controller import ModelPackageController
        from foundations_production.serving.rest_api_server import RestAPIServer

        self.model_package_controller = ModelPackageController()
        RestAPIServer()

    def test_add_new_model_package_in_manage_model_package_route(self):
        from foundations_production.serving.rest_api_server import RestAPIServer

        with patch.object(RestAPIServer, 'get_package_pool') as get_package_pool:
            get_package_pool.return_value = self.package_pool_mock
            self.model_package_controller.params = {'model_id': self.model_package_id, 'user_defined_model_name': 'fancy_model'}
            self.model_package_controller.post().evaluate()
            self.package_pool_mock.add_package.assert_called_with(self.model_package_id)
