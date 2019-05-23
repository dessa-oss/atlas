"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_contrib.set_job_resources import set_job_resources
from foundations_contrib.global_state import current_foundations_context

class TestSetJobResources(Spec):

    @let
    def num_gpus(self):
        return self.faker.random_int(0, 8)

    @let
    def ram(self):
        return self.faker.random.random() * 256

    @let
    def invalid_ram(self):
        return self.faker.random.random() * -1

    @let
    def job_resources(self):
        from foundations_internal.job_resources import JobResources
        return JobResources(self.num_gpus, self.ram)

    @tear_down
    def tear_down(self):
        current_foundations_context().reset_job_resources()

    def test_set_job_resources_sets_job_resources_object_in_current_foundations_context(self):
        set_job_resources(self.num_gpus, self.ram)
        job_resources = current_foundations_context().job_resources()
        self.assertEqual(self.job_resources, job_resources)

    def test_ram_set_less_than_or_equal_to_zero_throws_value_error(self):
        with self.assertRaises(ValueError) as error_context:
            set_job_resources(self.num_gpus, self.invalid_ram)
        
        error_message = 'Invalid RAM quantity. Please provide a RAM quantity greater than zero.'
        self.assertIn(error_message, error_context.exception.args)

