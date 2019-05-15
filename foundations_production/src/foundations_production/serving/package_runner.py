"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def run_model_package(model_package_id, communicator):
    import os
    from foundations_production.serving import create_job_workspace

    predictor = _create_predictor_for(model_package_id, communicator)
    create_job_workspace(model_package_id)
    os.chdir('/tmp/foundations_workspaces/{}'.format(model_package_id))

    if not predictor:
        return

    while True:
        json_input_data = communicator.get_action_request()
        if not _successful_run_of_json_predictions_for(model_package_id, communicator, predictor, json_input_data):
            return 

def _send_exception(exception, communicator):
    expected_return = {
        'name': str(type(exception).__name__),
        'value': str(exception)
    }
    communicator.set_response(expected_return)

def _create_predictor_for(model_package_id, communicator):
    from foundations_production.serving.inference.predictor import Predictor
    
    try:
        predictor = Predictor.predictor_for(model_package_id)
        communicator.set_response('SUCCESS: predictor created')
    except Exception as e:
        _send_exception(e, communicator)
        predictor =  None

    return predictor

def _successful_run_of_json_predictions_for(model_package_id, communicator, predictor, json_input_data):
    if json_input_data == 'STOP':
        return False
    try:
        json_predictions = predictor.json_predictions_for(json_input_data)
        communicator.set_response(json_predictions)
        return True
    except Exception as e:
        _send_exception(e, communicator)
        return False