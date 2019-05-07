"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.serving.package_runner import run_model_package, run_prediction

class TestPackageRunner(Spec):

    @let
    def fake_data(self):
        return self.faker.words()
    
    @let
    def prediction(self):
        return self.faker.word()
    
    @let
    def model_package_id(self):
        return self.faker.uuid4()
    
    mock_load_model_package = let_patch_mock('foundations_production.load_model_package')
    
    def test_run_prediction_runs_prediction_on_model_with_correct_data(self):
        model_package = Mock()
        model_package.model.predict = ConditionalReturn()
        model_package.model.predict.return_when(self.prediction, self.fake_data)

        actual_prediction = run_prediction(model_package, self.fake_data)
        self.assertEqual(self.prediction, actual_prediction)
    
    def test_run_model_package_loads_model_package(self):
        queue = Mock()
        run_model_package(self.model_package_id, queue)
        self.mock_load_model_package.assert_called_with(self.model_package_id)

        
        