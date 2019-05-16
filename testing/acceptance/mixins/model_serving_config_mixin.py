"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class ModelServingConfigMixin(Spec):

    @let
    def model_server_config_path(self):
        return 'model_server.config.yaml'

    def set_up_model_server_config(self):
        import os

        os.environ['MODEL_SERVER_CONFIG_PATH'] = self.model_server_config_path
        self._create_model_server_config_file()

    def _create_model_server_config_file(self):
        from acceptance.config import ARCHIVE_ROOT
        import yaml
        import os.path as path

        config_dictionary = {
            'job_deployment_env': 'local',
            'results_config': {
                'archive_end_point': 'local://' + path.dirname(ARCHIVE_ROOT)
            },
            'cache_config': {},
            'obfuscate_foundations': False
        }

        with open(self.model_server_config_path, 'w') as config_file:
            yaml.dump(config_dictionary, config_file)

    def tear_down_model_server_config(self):
        import os

        os.remove(self.model_server_config_path)
