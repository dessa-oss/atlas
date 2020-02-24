
from foundations_spec import *
import foundations

class TestSetJobResources(Spec):

    def test_set_job_resources_is_available_in_sdk(self):
        from foundations_contrib.set_job_resources import set_job_resources
        self.assertIs(set_job_resources, foundations.set_job_resources)

