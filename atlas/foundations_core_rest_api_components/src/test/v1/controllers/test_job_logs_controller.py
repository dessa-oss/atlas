

from foundations_spec import *

from foundations_core_rest_api_components.v1.controllers.job_logs_controller import JobLogsController

class TestJobLogsController(Spec):
    
    mock_get_job_logs = let_patch_mock_with_conditional_return('foundations_contrib.jobs.logs.job_logs')

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def job_logs(self):
        return self.faker.sentence()

    @let
    def controller(self):
        return JobLogsController()

    @set_up
    def set_up(self):
        self.mock_get_job_logs.return_when(self.job_logs, self.job_id)
        self.controller.params = { 'job_id': self.job_id }

    # @quarantine
    def test_index_returns_logs_for_job(self):
        self.assertEqual({'log': self.job_logs}, self.controller.index().as_json())
