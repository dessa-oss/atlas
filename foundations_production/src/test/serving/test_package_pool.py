"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.serving.package_pool import PackagePool
from foundations_production.serving.package_runner import run_model_package

class TestPackagePool(Spec):

    model_1_pipe = let_mock()
    model_2_pipe = let_mock()

    @let
    def model_id(self):
        return self.faker.uuid4()

    @let
    def model_2_id(self):
        return self.faker.uuid4()
    @let
    def fake_data(self):
        import pandas
        return pandas.DataFrame({self.faker.word(): self.faker.words()})
    
    @set_up
    def set_up(self):
        self.mock_process = self.patch('foundations_production.serving.restartable_process.RestartableProcess', ConditionalReturn())
        self.mock_process.return_when(self.model_1_pipe, target=run_model_package, args=(self.model_id))
        self.mock_process.return_when(self.model_2_pipe, target=run_model_package, args=(self.model_2_id))

    def test_package_pool_add_package_creates_new_process(self):
        package_pool = PackagePool(active_package_limit=1)
        package_pool.add_package(self.model_id)
        self.mock_process.assert_called_with(target=run_model_package, args=(self.model_id))
    
    def test_run_prediction_on_package_calls_correct_pipe(self):
        package_pool = PackagePool(active_package_limit=1)
        package_pool.add_package(self.model_id)
        package_pool.run_prediction_on_package(self.model_id, self.fake_data)
        self.model_1_pipe.send.assert_called_with(self.fake_data)

    def test_run_prediction_on_package_calls_coorect_pipe_when_multiple_packages(self):
        package_pool = PackagePool(active_package_limit=1)
        package_pool.add_package(self.model_id)
        package_pool.add_package(self.model_2_id)
        package_pool.run_prediction_on_package(self.model_id, self.fake_data)
        self.model_1_pipe.send.assert_called_with(self.fake_data)

