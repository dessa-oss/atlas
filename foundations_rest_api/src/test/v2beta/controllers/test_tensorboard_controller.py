"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
import os
from random import randint

import unittest
from mock import patch

from foundations.artifacts.syncable_directory import SyncableDirectory
from foundations_rest_api.v2beta.controllers.tensorboard_controller import TensorboardController
from foundations_rest_api.v2beta.models.property_model import PropertyModel
from foundations_spec import Spec, let, let_now, set_up, Mock

class TestTensorboardController(Spec):

    @let_now
    def config_manager(self):
        from foundations_contrib.config_manager import ConfigManager

        config_manager = ConfigManager()
        config_manager['TENSORBOARD_HOST'] = '10.103.113.163'
        return self.patch('foundations_contrib.global_state.config_manager', config_manager)

    @let
    def controller(self):
        return TensorboardController()
    
    @let
    def job_id(self):
        return [self.faker.uuid4()]

    @set_up
    def set_up(self):
        self.controller.params = {'tensorboard_locations': [{'job_id': self.job_id, 'synced_directory': 'tb_data'}]}

    @patch('requests.post', Mock(return_value=('Sucess', 200)))
    def test_tensorboard_controller_post(self):
        import requests
        self.controller.post()
        requests.post.assert_called_with(f'http://10.103.113.163/create_sym_links', json=self.controller.params)
