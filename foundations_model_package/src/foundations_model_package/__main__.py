"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_model_package.job import Job
from foundations_model_package.redis_actions import indicate_model_ran_to_redis
from foundations_model_package.resource_factories import prediction_resource, evaluate_resource, retrain_resource
from foundations_model_package.flask_app import flask_app
from foundations_model_package.entrypoint_loader import EntrypointLoader
from foundations_model_package.retrain_driver import RetrainDriver

def main():
    import os

    from foundations import config_manager
    configuration = config_manager.config()
    
    if 'REDIS_URL' in os.environ:
        configuration['redis_url'] = os.environ['REDIS_URL']
    else:
        configuration['redis_url'] = 'redis://redis'

    job = Job(os.environ['JOB_ID'])
    prediction_function = EntrypointLoader(job).entrypoint_function('predict')

    try:
        evaluate_function = EntrypointLoader(job).entrypoint_function('evaluate')
    except Exception:
        evaluate_function = None

    try:
        entrypoint_loader = EntrypointLoader(job)
        retrain_function = entrypoint_loader.entrypoint_function('retrain')
        retrain_function_name = entrypoint_loader.function_name('retrain')
        retrain_module_name = entrypoint_loader.module_name('retrain')

        retrain_driver = RetrainDriver(retrain_module_name, retrain_function_name)
            
    except Exception:
        retrain_driver = None

    root_model_serving_resource = prediction_resource(prediction_function)
    predict_model_serving_resource = prediction_resource(prediction_function)
    model_evaluation_resource = evaluate_resource(evaluate_function)
    model_retrain_resource = retrain_resource(retrain_driver)
    app = flask_app(root_model_serving_resource, predict_model_serving_resource, model_evaluation_resource, model_retrain_resource)

    indicate_model_ran_to_redis(job.id())

    print('Model server running successfully')
    app.run(use_reloader=False, debug=True, port=80, host='0.0.0.0')

def _hack_for_cleaning_up_logs():
    import click
    import logging

    def _break_click_echo(*args, **kwargs):
        pass

    click.echo = _break_click_echo
    click.secho = _break_click_echo

    log = logging.getLogger('werkzeug')
    # log.disabled = True

if __name__ == '__main__':
    main()