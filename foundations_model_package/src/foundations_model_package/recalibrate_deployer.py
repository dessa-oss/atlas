
class RecalibrateDeployer(object):

    def __init__(self, job_id, project_name, model_name, project_directory):
        self.job_id = job_id
        self.project_name = project_name
        self.model_name = model_name
        self.project_directory = project_directory

    def start(self):
        from foundations_contrib.cli.orbit_model_package_server import deploy

        _wait_for_job_to_complete(self.job_id)

        deploy(project_name=self.project_name, model_name=self.model_name, project_directory=self.project_directory, env='scheduler')

def _wait_for_statuses(job_id, statuses, error_message):
    import time

    time_elapsed = 0
    timeout = 60

    while _job_status(job_id) in statuses:
        if time_elapsed >= timeout:
            raise AssertionError(error_message)

        time_elapsed += 5
        time.sleep(5)

def _job_status(job_id):
    from foundations_scheduler.pod_fetcher import get_latest_for_job
    from foundations_scheduler_core.kubernetes_api_wrapper import KubernetesApiWrapper

    _core_api = KubernetesApiWrapper().core_api()

    pod = get_latest_for_job(_core_api, job_id)

    if pod is None:
        return 'Pending'
    else:
        return pod.status.phase

def _wait_for_job_to_complete(job_id):
    _wait_for_statuses(job_id, ['Pending', 'Running'], 'job did not finish')