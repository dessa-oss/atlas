"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def retrain_resource(retrain_driver):
    from flask_restful import Resource
    from uuid import uuid4
    from flask import request

    class _RetrainResource(Resource):
        
        def post(self):
            import os
            import foundations
            from foundations.global_state import message_router
            from foundations_model_package.retrain_deployer import RetrainDeployer

            if retrain_driver is None:
                return {'error': 'retrain not set in manifest'}, 404

            project_name = os.environ['PROJECT_NAME']
            model_name = os.environ['MODEL_NAME']
            project_directory = os.getcwd()

            with retrain_driver as driver_file:
                entrypoint = driver_file

            params = request.json

            job_deployment = foundations.submit(project_name=project_name, entrypoint=entrypoint, params=params)
            job_id = job_deployment.job_name()

            retrain_deployer = RetrainDeployer(job_id, project_name, model_name, project_directory)
            message_router.add_listener(retrain_deployer, 'complete_job')

            return {'job_id': job_id}, 202

    _RetrainResource.__name__ = f'_RetrainResource_{uuid4()}'

    return _RetrainResource