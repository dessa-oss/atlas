"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def run_model_package(model_package_id, communicator):
    from foundations_production.serving.inference.predictor import Predictor
    import sys
    
    try:
        predictor = Predictor.predictor_for(model_package_id)
        communicator.set_response('SUCCESS: predictor created')
    except Exception as e:
        _send_exception(e, communicator)
        return

    while True:
        json_input_data = communicator.get_action_request()
        if json_input_data == 'STOP':
            return
        try:
            json_predictions = predictor.json_predictions_for(json_input_data)
            communicator.set_response(json_predictions)
        except Exception as e:
            _send_exception(e, communicator)
            return

def _send_exception(exception, communicator):
    expected_return = {
        'name': str(type(exception).__name__),
        'value': str(exception)
    }
    communicator.set_response(expected_return)
