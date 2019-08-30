
class RetrainDeployer(object):

    def __init__(self, job_id, project_name, model_name, project_directory):
        self.job_id = job_id
        self.project_name = project_name
        self.model_name = model_name
        self.project_directory = project_directory

    def call(self, message, timestamp, metadata):
        from foundations_contrib.cli.orbit_model_package_server import deploy

        if message['job_id'] == self.job_id:
            deploy(project_name=self.project_name, model_name=self.model_name, project_directory=self.project_directory, env='scheduler')
        