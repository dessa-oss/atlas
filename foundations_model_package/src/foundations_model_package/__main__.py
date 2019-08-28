"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_model_package.job import Job
from foundations_model_package.redis_actions import indicate_model_ran_to_redis
from foundations_model_package.resource_factories import prediction_resource, evaluate_resource
from foundations_model_package.flask_app import flask_app
from foundations_model_package.entrypoint_loader import EntrypointLoader

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

    root_model_serving_resource = prediction_resource(prediction_function)
    predict_model_serving_resource = prediction_resource(prediction_function)
    model_evaluation_resource = evaluate_resource(evaluate_function)
    app = flask_app(root_model_serving_resource, predict_model_serving_resource, model_evaluation_resource)

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