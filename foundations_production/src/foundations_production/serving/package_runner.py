"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def run_model_package(model_package_id, communicator):
    import os
    from foundations_production.serving import extract_job_source, workspace_path, prepare_job_workspace
    from foundations_production.exceptions import MissingModelPackageException

    _set_job_id()

    workspace_path = workspace_path(model_package_id)

    try:
        prepare_job_workspace(model_package_id)
        os.chdir(workspace_path)
        predictor = _create_predictor_for(model_package_id, communicator)
    except FileNotFoundError:
        missing_model_package_exception = MissingModelPackageException(model_package_id)
        _send_exception(missing_model_package_exception, communicator)
        return
    except Exception as e:
        _send_exception(e, communicator)
        return

    while True:
        json_input_data = communicator.get_action_request()
        if not _successful_run_of_json_predictions_for(model_package_id, communicator, predictor, json_input_data):
            return 

def _set_job_id():
    from foundations_contrib.global_state import current_foundations_context
    current_foundations_context().pipeline_context().file_name = 'package_running'

def _send_exception(exception, communicator):
    expected_return = {
        'name': str(type(exception).__name__),
        'value': str(exception)
    }
    communicator.set_response(expected_return)

def _create_predictor_for(model_package_id, communicator):
    from foundations_production.serving.inference.predictor import Predictor
    
    predictor = Predictor.predictor_for(model_package_id)
    communicator.set_response('SUCCESS: predictor created')

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