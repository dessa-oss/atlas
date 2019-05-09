"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_production.serving import create_retraining_job

class TestCreateRetrainingJob(Spec):
    
    mock_data_from_file = let_patch_mock('foundations_production.serving.data_from_file.data_from_file', ConditionalReturn())
    mock_load_model_package = let_patch_mock('foundations_production.load_model_package', ConditionalReturn())

    mock_features = let_mock()
    mock_preprocessed_features = let_mock()
    mock_targets = let_mock()

    mock_preprocessor = let_mock()
    mock_production_model = let_mock()

    mock_retrained_model = let_mock()

    mock_preprocessor_callback = ConditionalReturn()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def fake_features_path(self):
        return self.faker.file_path()

    @let
    def fake_targets_path(self):
        return self.faker.file_path()

    @let
    def preprocessor_callback(self):
        import foundations

        callback = ConditionalReturn()
        callback.return_when(self.mock_preprocessed_features, self.mock_features)

        def _preprocessor_internal_callback(*args, **kwargs):
            return callback(*args, **kwargs)

        return foundations.create_stage(_preprocessor_internal_callback)

    @let
    def production_model_retrain_callback(self):
        import foundations

        callback = ConditionalReturn()
        callback.return_when(self.mock_retrained_model, self.mock_preprocessed_features, self.mock_targets)

        def _production_model_retrain_internal_callback(*args, **kwargs):
            return callback(*args, **kwargs)

        return foundations.create_stage(_production_model_retrain_internal_callback)

    @let
    def model_package(self):
        from foundations_production.model_package import ModelPackage
        return ModelPackage(model=self.mock_production_model, preprocessor=self.mock_preprocessor)

    @set_up
    def set_up(self):
        self.mock_data_from_file.return_when(self.mock_features, self.fake_features_path)
        self.mock_data_from_file.return_when(self.mock_targets, self.fake_targets_path)

        self.mock_load_model_package.return_when(self.model_package, self.job_id)

        self.mock_preprocessor.side_effect = self.preprocessor_callback

        self.mock_production_model.retrain.side_effect = self.production_model_retrain_callback

        self._retraining_job = create_retraining_job(
            self.job_id,
            features_location=self.fake_features_path,
            targets_location=self.fake_targets_path
        )

    def test_retraining_job_loads_files_only_when_job_executed(self):
        self.mock_data_from_file.assert_not_called()

    def test_retraining_job_sets_preprocessor_inference_mode_to_false(self):
        self.mock_preprocessor.set_inference_mode.assert_called_once_with(False)

    def test_retraining_job_retrains_model_when_job_executed(self):
        retrained_model = self._retraining_job.run_same_process()
        self.assertEqual(self.mock_retrained_model, retrained_model)