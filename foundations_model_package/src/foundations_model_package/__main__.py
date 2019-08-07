"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
import os

from foundations_model_package.job import Job

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

def main():
    _hack_for_cleaning_up_logs()

    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    api = Api(app)

    job = Job(os.environ['JOB_ID'])

    def move_to_job_directory():
        import sys
        import os

        root_of_the_job = job.root()
        if not os.path.exists(root_of_the_job):
            raise Exception(f'Job, {job.id()} not found!')

        sys.path.insert(0, root_of_the_job)
        os.chdir(root_of_the_job)

    def add_module_to_sys_path(module_name):
        import sys
        import os.path

        module_path = module_name.replace('.', '/')
        module_directory = os.path.dirname(module_path)
        if module_directory:
            module_directory = f"{job.root()}/{module_directory}"
            sys.path.insert(0, module_directory)

    def load_prediction_function(manifest):
        import importlib

        move_to_job_directory()
        module_name, function_name = _module_name_and_function_name(manifest)
        add_module_to_sys_path(module_name)

        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError as error:
            raise Exception('Prediction module defined in manifest file could not be found!') from error
        except Exception as error:
            raise Exception('Unable to load prediction module from manifest') from error

        function = getattr(module, function_name, None)

        if not function:
            raise Exception('Prediction function defined in manifest file could not be found!')

        return function

    def indicate_model_ran_to_redis():
        from foundations_contrib.global_state import redis_connection

        job_id_to_track = job.id()
        redis_connection.incr(f'models:{job_id_to_track}:served')

    prediction_function = load_prediction_function(job.manifest())
    indicate_model_ran_to_redis()

    class ServeModel(Resource):
        def get(self):
            return {'message': 'still alive'}

        def post(self):
            data = dict(request.json)
            return prediction_function(**data)

    api.add_resource(ServeModel, '/')

    print('Model server running successfully')

    app.logger.disabled = True
    app.run(debug=False, port=80, host='0.0.0.0')

if __name__ == '__main__':
    main()