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

            project_name = os.environ['PROJECT_NAME']

            with retrain_driver as driver_file:
                entrypoint = driver_file

            params = request.json

            job_deployment = foundations.submit(project_name=project_name, entrypoint=entrypoint, params=params)
            job_id = job_deployment.job_name()

            return {'job_id': job_id}, 202

    _RetrainResource.__name__ = f'_RetrainResource_{uuid4()}'

    return _RetrainResource