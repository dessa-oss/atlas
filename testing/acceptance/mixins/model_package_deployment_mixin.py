"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import acceptance.fixtures.train_model_package as train_model_package


class ModelPackageDeploymentMixin(Spec):

    def deploy_model_package(self):
        job = train_model_package.validation_predictions.run()
        job.wait_for_deployment_to_complete()
        return job.job_name()
