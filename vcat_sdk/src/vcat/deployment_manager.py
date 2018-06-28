"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class DeploymentManager(object):

    def deploy(self, deployment_config, job_name, job):
        deployment = self._create_deployment(job_name, job)
        deployment.config().update(deployment_config)
        deployment.deploy()
        return deployment

    def _create_deployment(self, job_name, job):
        from vcat.job_source_bundle import JobSourceBundle
        from vcat.global_state import config_manager

        deployment_constructor, constructor_args, constructor_kwargs = config_manager.reflect_constructor(
            'deployment', 'deployment', DeploymentManager._create_default_deployment)

        config = config_manager.config()
        job_source_bundle_dict = config['job_source_bundle']
        job_source_bundle = JobSourceBundle.from_dict(job_source_bundle_dict)

        return deployment_constructor(job_name, job, job_source_bundle, *constructor_args, **constructor_kwargs)

    @staticmethod
    def _create_default_deployment(job_name, job, job_source_bundle):
        from vcat.local_shell_job_deployment import LocalShellJobDeployment
        return LocalShellJobDeployment(job_name, job, job_source_bundle)
