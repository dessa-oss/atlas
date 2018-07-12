"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class DeploymentManager(object):

    def simple_deploy(self, stage, job_params):
        import uuid

        from vcat.global_state import deployment_manager
        from vcat.job import Job

        job_name = str(uuid.uuid4())
        job = Job(stage, **job_params)
        return deployment_manager.deploy({}, job_name, job)

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

        job_source_bundle = JobSourceBundle.for_deployment()

        return deployment_constructor(job_name, job, job_source_bundle, *constructor_args, **constructor_kwargs)

    @staticmethod
    def _create_default_deployment(job_name, job, job_source_bundle):
        from vcat.local_shell_job_deployment import LocalShellJobDeployment
        return LocalShellJobDeployment(job_name, job, job_source_bundle)
