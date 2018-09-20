"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class DeploymentManager(object):

    def __init__(self):
        self._scheduler = None

    def simple_deploy(self, stage, job_name, job_params):
        import uuid

        from foundations.global_state import deployment_manager
        from foundations.job import Job

        if not job_name:
            job_name = str(uuid.uuid4())
        job = Job(stage, **job_params)
        return deployment_manager.deploy({}, job_name, job)

    def deploy(self, deployment_config, job_name, job):
        deployment = self._create_deployment(job_name, job)
        deployment.config().update(deployment_config)
        deployment.deploy()
        return deployment

    def scheduler(self):
        from foundations.scheduler import Scheduler

        if self._scheduler is None:
            deployment_constructor, _, _ = self._deployment_constructor_and_args_and_kwargs()
            self._scheduler = Scheduler(deployment_constructor.scheduler_backend())
            
        return self._scheduler

    def _create_deployment(self, job_name, job):
        from foundations.job_source_bundle import JobSourceBundle

        deployment_constructor, constructor_args, constructor_kwargs = self._deployment_constructor_and_args_and_kwargs()

        job_source_bundle = JobSourceBundle.for_deployment()

        return deployment_constructor(job_name, job, job_source_bundle, *constructor_args, **constructor_kwargs)

    def _deployment_constructor_and_args_and_kwargs(self):
        from foundations.global_state import config_manager
        return config_manager.reflect_constructor('deployment', 'deployment', DeploymentManager._create_default_deployment)

    @staticmethod
    def _create_default_deployment(job_name, job, job_source_bundle):
        from foundations.local_shell_job_deployment import LocalShellJobDeployment
        return LocalShellJobDeployment(job_name, job, job_source_bundle)
