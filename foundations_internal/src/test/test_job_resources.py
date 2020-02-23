
from foundations_spec import *

from foundations_internal.job_resources import JobResources

class TestJobResources(Spec):

    @let
    def num_gpus(self):
        return self.faker.random_int(0, 8)

    @let
    def ram(self):
        return self.faker.random.random() * 256

    @set_up
    def set_up(self):
        self._job_resources = JobResources(self.num_gpus, self.ram)

    def test_get_number_of_gpus_from_job_resources(self):
        self.assertEqual(self.num_gpus, self._job_resources.num_gpus)

    def test_get_ram_from_job_resources(self):
        self.assertEqual(self.ram, self._job_resources.ram)