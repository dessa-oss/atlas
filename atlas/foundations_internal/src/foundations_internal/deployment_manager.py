

class DeploymentManager(object):

    def __init__(self, config_manager):
        self._config_manager = config_manager

    def simple_deploy(self, foundations_context, job_name, job_params):
        import uuid

        from foundations.job import Job

        if not job_name:
            job_name = str(uuid.uuid4())
        job = Job(foundations_context, **job_params)

        deployment = self.deploy({}, job_name, job)
        self._record_project(foundations_context)
        return deployment

    def deploy(self, deployment_config, job_name, job):
        from foundations import log_manager
        from foundations.global_state import current_foundations_context

        logger = log_manager.get_logger(__name__)

        deployment = self._create_deployment(job_name, job)
        deployment.config().update(deployment_config)
        project_name = current_foundations_context().project_name()

        deployment.deploy()
        logger.info("Job submitted with ID '{}' in project '{}'.".format(job_name, project_name))

        return deployment

    def _record_project(self, foundations_context):
        constructor, constructor_args, constructor_kwargs = self.project_listing_constructor_and_args_and_kwargs()
        listing = constructor(*constructor_args, **constructor_kwargs)
        listing.track_pipeline(
            foundations_context.project_name())

    def _create_deployment(self, job_name, job):
        from foundations_contrib.job_source_bundle import JobSourceBundle

        deployment_constructor, constructor_args, constructor_kwargs = self._deployment_constructor_and_args_and_kwargs()

        job_source_bundle = JobSourceBundle.for_deployment()

        return deployment_constructor(job_name, job, job_source_bundle, *constructor_args, **constructor_kwargs)

    def _deployment_constructor_and_args_and_kwargs(self):
        return self._config_manager.reflect_constructor('deployment', 'deployment', DeploymentManager._create_default_deployment)

    def project_listing_constructor_and_args_and_kwargs(self):
        return self._config_manager.reflect_constructor('project_listing', 'project_listing', DeploymentManager._create_default_project_listing)

    @staticmethod
    def _create_default_project_listing():
        from foundations_contrib.null_pipeline_archive_listing import NullPipelineArchiveListing
        return NullPipelineArchiveListing()

    @staticmethod
    def _create_default_deployment(job_name, job, job_source_bundle):
        from foundations_local_docker_scheduler_plugin.job_deployment import JobDeployment
        return JobDeployment(job_name, job, job_source_bundle)
