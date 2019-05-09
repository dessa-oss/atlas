"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def run_model_package(model_package_id, communicator):
    from foundations_production import load_model_package
    model_package = load_model_package(model_package_id)

    while True:
        data = communicator.receive_from_server()
        if data == 'STOP':
            return
        prediction = run_prediction(model_package, data)
        communicator.send_to_server(prediction)

def run_prediction(model_package, data):
    return model_package.model.predict(data)