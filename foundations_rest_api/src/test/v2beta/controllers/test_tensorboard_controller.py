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
from foundations_spec import Spec, let

class TestTensorboardController(Spec):

    _namespace = 'foundations-scheduler-test'

    @let
    def syncable_directory(self):
        SyncableDirectory()
    @let
    def controller(self):
        return TensorboardController()
    
    @let
    def job_ids(self):
        return [self.faker.uuid4()]

