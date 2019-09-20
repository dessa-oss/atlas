"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def recalibrate_resource(recalibrate_driver):
    from flask_restful import Resource
    from uuid import uuid4
    from flask import request

    class _RecalibrateResource(Resource):
        
        def post(self):
            import os
            import foundations
            import subprocess
            from foundations.global_state import message_router
            from foundations_model_package.recalibrate_deployer import RecalibrateDeployer
            from kubernetes import config

            if recalibrate_driver is None:
                return {'error': 'recalibrate not set in manifest'}, 404

            params = dict(request.json)
            project_name = os.environ['PROJECT_NAME']
            model_name = params.pop('model-name')
            project_directory = os.getcwd()

            with recalibrate_driver as driver_file:
                entrypoint = driver_file

                config.load_incluster_config()
                job_deployment = foundations.submit(project_name=project_name, entrypoint=entrypoint, params=params)
                job_id = job_deployment.job_name()

                retrain_deployer = RecalibrateDeployer(job_id, project_name, model_name, project_directory)

                retrain_deployer.start()

                return {'job_id': job_id}, 202

    _RecalibrateResource.__name__ = f'_RecalibrateResource_{uuid4()}'

    return _RecalibrateResource