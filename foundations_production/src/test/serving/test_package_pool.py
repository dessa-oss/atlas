"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.serving.package_pool import PackagePool

class TestPackagePool(Spec):

    mock_process = let_patch_mock('foundations_production.serving.restartable_process.RestartableProcess')

    @let
    def model_id(self):
        return self.faker.uuid4()

    def test_package_pool_add_package_creates_new_process(self):
        from foundations_production.serving.package_runner import run_model_package

        package_pool = PackagePool(active_package_limit=1)
        package_pool.add_package(self.model_id)
        self.mock_process.assert_called_with(target=run_model_package, args=(self.model_id))
