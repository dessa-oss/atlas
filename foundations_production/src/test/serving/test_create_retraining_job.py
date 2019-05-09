"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_production.serving import create_retraining_job

class TestCreateRetrainingJob(Spec):
    
    mock_data_from_file = let_patch_mock('foundations_production.serving.data_from_file.data_from_file')
    mock_load_model_package = let_patch_mock('foundations_production.load_model_package')

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def fake_features_path(self):
        return self.faker.file_path()

    @let
    def fake_targets_path(self):
        return self.faker.file_path()

    @set_up
    def set_up(self):
        self._retraining_job = create_retraining_job(self.job_id, features_location=self.fake_features_path, targets_location=self.fake_targets_path)

    def test_retraining_job_loads_features(self):
        self._test_file_loaded(self.fake_features_path)

    def test_retraining_job_loads_targets(self):
        self._test_file_loaded(self.fake_targets_path)

    def test_retraining_job_loads_files_only_when_job_executed(self):
        self.mock_data_from_file.assert_not_called()

    def test_retraining_job_loads_model_package(self):
        self.mock_load_model_package.assert_called_with(self.job_id)

    def _test_file_loaded(self, file_name):
        self._retraining_job.run_same_process()
        self.mock_data_from_file.assert_any_call(file_name)