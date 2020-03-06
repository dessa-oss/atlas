
class JobController(object):

    # TODO: add unit tests as previous ones were k8s based
    def delete(self):
        from foundations_core_rest_api_components.response import Response
        from foundations_core_rest_api_components.lazy_result import LazyResult
        from foundations_contrib.global_state import config_manager

        job_deployment_class = config_manager['deployment_implementation']['deployment_type']
        job_deployment = job_deployment_class(self.job_id, None, None)

        job_status = job_deployment.get_job_status()

        if job_status is None:
            return Response('Jobs', LazyResult(lambda: f'Job {self.job_id} is in an unknown state'))
        if not (job_status == 'completed' or job_status == 'failed'):
            return Response('Jobs', LazyResult(lambda: f'Job {self.job_id} is not completed or failed'))

        if all(job_deployment.cancel_jobs([self.job_id]).values()):
            return Response('Jobs', LazyResult(lambda: f'Job {self.job_id} successfully deleted'))
        return Response('Jobs', LazyResult(lambda: f'Job {self.job_id} could not be deleted'))

    @property
    def job_id(self):
        return self.params['job_id']
