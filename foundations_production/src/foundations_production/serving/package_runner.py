"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def run_model_package(model_package_id, communicator):
    from foundations_production.serving.inference.predictor import Predictor
    
    predictor = Predictor.predictor_for(model_package_id)

    while True:
        json_input_data = communicator.get_action_request()
        if json_input_data == 'STOP':
            return
        json_predictions = predictor.json_predictions_for(json_input_data)
        communicator.set_response(json_predictions)
