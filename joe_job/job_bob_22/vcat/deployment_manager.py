class DeploymentManager(object):

    def deploy(self, deployment_config, job_name, job, job_source_bundle):
        deployment = self._create_deployment(job_name, job, job_source_bundle)
        deployment.config().update(deployment_config)
        deployment.deploy()
        return deployment

    def _create_deployment(self, job_name, job, job_source_bundle):
        from vcat.global_state import config_manager

        deployment_constructor, _, _ = config_manager.reflect_constructor(
            'deployment', 'deployment', DeploymentManager._create_default_deployment)
        return deployment_constructor(job_name, job, job_source_bundle)

    @staticmethod
    def _create_default_deployment(job_name, job, job_source_bundle):
        from vcat.local_shell_job_deployment import LocalShellJobDeployment
        return LocalShellJobDeployment(job_name, job, job_source_bundle)
