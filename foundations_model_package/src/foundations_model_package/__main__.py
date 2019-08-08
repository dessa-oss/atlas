"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def main():
    import os

    from foundations_model_package.job import Job
    from foundations_model_package.redis_actions import indicate_model_ran_to_redis
    from foundations_model_package.resource_factories import prediction_resource
    from foundations_model_package.flask_app import flask_app

    _hack_for_cleaning_up_logs()

    job = Job(os.environ['JOB_ID'])

    prediction_function = _load_prediction_function(job)

    root_model_serving_resource = prediction_resource(prediction_function)
    predict_model_serving_resource = prediction_resource(prediction_function)
    app = flask_app(root_model_serving_resource, predict_model_serving_resource)
    indicate_model_ran_to_redis(job.id())

    print('Model server running successfully')

    app.run(debug=False, port=80, host='0.0.0.0')

def _hack_for_cleaning_up_logs():
    import click
    import logging

    def _break_click_echo(*args, **kwargs):
        pass

    click.echo = _break_click_echo
    click.secho = _break_click_echo

    log = logging.getLogger('werkzeug')
    log.disabled = True

def _module_name_and_function_name(manifest):
    prediction_definition = manifest['entrypoints']['predict']
    return prediction_definition['module'], prediction_definition['function']

def _load_prediction_function(job):
    import importlib

    from foundations_model_package.entrypoint_loader import EntrypointLoader
    from foundations_model_package.importlib_wrapper import load_function_from_module

    EntrypointLoader(job).entrypoint_function()
    module_name, function_name = _module_name_and_function_name(job.manifest())

    return load_function_from_module(module_name, function_name)

if __name__ == '__main__':
    main()