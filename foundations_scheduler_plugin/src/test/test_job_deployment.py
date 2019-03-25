"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *

from foundations_scheduler_plugin.job_deployment import JobDeployment

class TestJobDeployment(Spec):

    @let
    def config_manager_config(self):
        return self.faker.pydict()

    @let_now
    def config_manager(self):
        from foundations_contrib.config_manager import ConfigManager

        config_manager = ConfigManager()
        config_manager.config().update(self.config_manager_config)
        return self.patch('foundations_contrib.global_state.config_manager', config_manager)

    @let
    def deployment(self):
        return JobDeployment(self.job_id, self.job, self.job_source_bundle)

    @let
    def job_id(self):
        from uuid import uuid4
        return str(uuid4())

    job = let_mock()
    job_source_bundle = let_mock()

    def test_stores_config_with_manager_config(self):
        self.assertDictContainsSubset(
            self.config_manager_config,
            self.deployment.config()
        )

    def test_stores_config_with_deployment_mode_set(self):
        self.assertEqual(True, self.deployment.config()['_is_deployment'])

    def test_scheduler_method_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            JobDeployment.scheduler_backend()

    def test_job_name_is_job_id(self):
        self.assertEqual(self.job_id, self.deployment.job_name())