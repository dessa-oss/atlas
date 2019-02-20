"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

from foundations_contrib.job_bundler import JobBundler


class AWSJobDeployment(object):

    def __init__(self, job_name, job, job_source_bundle, code_bucket_name, result_bucket_name):
        from foundations.bucket_job_deployment import BucketJobDeployment
        from foundations_aws.aws_bucket import AWSBucket

        self._deployment = BucketJobDeployment(job_name, job, job_source_bundle, AWSBucket(
            code_bucket_name), AWSBucket(result_bucket_name))

    def config(self):
        return self._deployment.config()

    def job_name(self):
        return self._deployment.job_name()

    def deploy(self):
        return self._deployment.deploy()

    def is_job_complete(self):
        return self._deployment.is_job_complete()

    def fetch_job_results(self):
        return self._deployment.fetch_job_results()

    def get_job_status(self):
        import foundations.constants as constants
        if not self.is_job_complete():
            return constants.deployment_running
        else:
            results = self.fetch_job_results()

            try:
                error_information = results["global_stage_context"]["error_information"]

                if error_information is not None:
                    return constants.deployment_error
                else:
                    return constants.deployment_completed
            except:
                return constants.deployment_error