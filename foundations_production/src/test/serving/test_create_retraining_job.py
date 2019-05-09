"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_production.serving import create_retraining_job

class TestCreateRetrainingJob(Spec):
    
    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def fake_features_path(self):
        return self.faker.file_path()

    @let
    def fake_targets_path(self):
        return self.faker.file_path()

    def test_retraining_job_loads_features(self):
        mock_data_from_file = self.patch('foundations_production.serving.data_from_file.data_from_file', Mock())

        job = create_retraining_job(self.job_id, features_location=self.fake_features_path, targets_location=self.fake_targets_path)
        job.run_same_process()

        mock_data_from_file.assert_any_call(self.fake_features_path)

    def test_retraining_job_loads_features_only_when_job_executed(self):
        mock_data_from_file = self.patch('foundations_production.serving.data_from_file.data_from_file', Mock())

        job = create_retraining_job(self.job_id, features_location=self.fake_features_path, targets_location=self.fake_targets_path)

        mock_data_from_file.assert_not_called()

    def test_retraining_job_loads_targets(self):
        mock_data_from_file = self.patch('foundations_production.serving.data_from_file.data_from_file', Mock())

        job = create_retraining_job(self.job_id, features_location=self.fake_features_path, targets_location=self.fake_targets_path)
        job.run_same_process()

        mock_data_from_file.assert_any_call(self.fake_targets_path)

    def test_retraining_job_loads_targets_only_when_job_executed(self):
        mock_data_from_file = self.patch('foundations_production.serving.data_from_file.data_from_file', Mock())

        job = create_retraining_job(self.job_id, features_location=self.fake_features_path, targets_location=self.fake_targets_path)

        mock_data_from_file.assert_not_called()