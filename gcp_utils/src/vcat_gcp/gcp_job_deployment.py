"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.job_bundler import JobBundler


class GCPJobDeployment(object):

    def __init__(self, job_name, job, job_source_bundle, code_bucket_name, result_bucket_name):
        from vcat.bucket_job_deployment import BucketJobDeployment
        from vcat_gcp.gcp_bucket import GCPBucket

        self._deployment = BucketJobDeployment(job_name, job, job_source_bundle, GCPBucket(
            code_bucket_name), GCPBucket(result_bucket_name))

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
        if not self.is_job_complete():
            return "Running"
        else:
            results = self.fetch_job_results()

            try:
                error_information = results["global_stage_context"]["error_information"]

                if error_information is not None:
                    return "Error"
                else:
                    return "Completed"
            except:
                return "Error"