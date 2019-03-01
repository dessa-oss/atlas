"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import os

class ResourcesObfuscationController(object):

    def __init__(self, config):
        self._module_directory = os.path.dirname(os.path.abspath(__file__))
        self._resource_directory = os.path.join(self._module_directory, "resources")

    def get_resources(self):
        return self._resource_directory