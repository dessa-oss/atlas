"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""
from foundations_production.serving.api_resource import api_resource
from foundations_rest_api.response import Response
from foundations_rest_api.lazy_result import LazyResult

@api_resource('/v1/<user_defined_model_name>/model')
class RetrainModelPackageController(object):

    def get(self):
        if not self._model_package_exists():
            return Response.constant('model package not found', status=404)
        return Response.constant('response')

    def put(self):
        def callback():
            from foundations_production.serving.rest_api_server_provider import get_rest_api_server

            rest_api_server = get_rest_api_server()
            model_package_mapping = rest_api_server.get_model_package_mapping()
            user_defined_model_name = self.params['user_defined_model_name']
            features_location = self.params['features_file']
            targets_location = self.params['targets_file']

            model_id = model_package_mapping[user_defined_model_name]
            retraining_job_deployment = self._deploy_retraining_job(model_id, targets_location, features_location)
            return {'created_job_uuid': retraining_job_deployment.job_name()}

        if not self._model_package_exists():
            return Response.constant('model package not found', status=404)

        return Response('retrain_model_package_controller', LazyResult(callback), status=202)

    def _model_package_exists(self):
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server

        rest_api_server = get_rest_api_server()
        model_package_mapping = rest_api_server.get_model_package_mapping()

        return self.params['user_defined_model_name'] in model_package_mapping

    def _deploy_retraining_job(self, model_package_id, targets_location, features_location):
        from foundations_production.serving import create_retraining_job

        retraining_job = create_retraining_job(model_package_id, targets_location=targets_location, features_location=features_location)
        return retraining_job.run()
