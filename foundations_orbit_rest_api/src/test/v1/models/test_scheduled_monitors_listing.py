
from foundations_spec import *

from foundations_orbit_rest_api.v1.models.scheduled_monitors_listing import ScheduledMonitorsListing

class TestScheduledMonitorsListing(Spec):

    mock_environ = let_patch_mock('os.environ')
    mock_cron_job_scheduler_class = let_patch_mock_with_conditional_return('from foundations_local_docker_scheduler_plugin.cron_job_scheduler.CronJobScheduler')
    
    @let
    def project_name(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        self.mock_environ.get.return_value = 'http://localhost:5000'
        self.mock_cron_job_scheduler = Mock()
        self.mock_cron_job_scheduler_class.return_when(self.mock_cron_job_scheduler, 'http://localhost:5000')