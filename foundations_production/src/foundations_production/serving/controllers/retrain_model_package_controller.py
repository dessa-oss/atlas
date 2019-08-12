"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""
from foundations_core_rest_api_components.response import Response
from foundations_core_rest_api_components.lazy_result import LazyResult

from foundations_production.serving.api_resource import api_resource
from foundations_production.serving.controllers.exceptions_as_http_errors import exceptions_as_http_errors
from foundations_production.serving.controllers.controller_mixin import ControllerMixin


@api_resource('/v1/<user_defined_model_name>/model/')
class RetrainModelPackageController(ControllerMixin):

    def get(self):

        @exceptions_as_http_errors
        def callback():
            self._get_model_id_from_model_package_mapping()
            return 'response'

        return Response('get_model_package_weights', LazyResult(callback), status=200)

    def put(self):

        @exceptions_as_http_errors
        def callback():
            model_package_id = self._get_model_id_from_model_package_mapping()
            retraining_job_deployment = self._deploy_retraining_job(model_package_id)
            return {'created_job_uuid': retraining_job_deployment.job_name()}

        return Response('retrain_model_package_controller', LazyResult(callback), status=202)

    def _deploy_retraining_job(self, model_package_id):
        import os
        from foundations_production.serving import create_retraining_job, workspace_path, prepare_job_workspace
        from foundations_internal.working_directory_stack import WorkingDirectoryStack

        features_location = self.params['features_file']
        targets_location = self.params['targets_file']

        with WorkingDirectoryStack():
            prepare_job_workspace(model_package_id)
            os.chdir(workspace_path(model_package_id))
            retraining_job = create_retraining_job(model_package_id, targets_location=targets_location, features_location=features_location)
            job_deployment = retraining_job.run()

        return job_deployment
