
from foundations_spec import *

from foundations_contrib.set_job_resources import set_job_resources
from foundations_contrib.global_state import current_foundations_context
from foundations_internal.job_resources import JobResources

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
    def non_integer_gpu(self):
        return self.faker.random.random()

    @let
    def negative_gpus(self):
        return self.faker.random_int(-1000000, -1)

    @let
    def job_resources(self):
        return JobResources(self.num_gpus, self.ram)

    @let
    def default_job_resources(self):
        return JobResources(1, None)

    @tear_down
    def tear_down(self):
        current_foundations_context().reset_job_resources()

    def test_set_job_resources_sets_job_resources_object_in_current_foundations_context(self):
        set_job_resources(self.num_gpus, self.ram)
        job_resources = current_foundations_context().job_resources
        self.assertEqual(self.job_resources, job_resources)

    def test_ram_set_less_than_or_equal_to_zero_throws_value_error(self):
        with self.assertRaises(ValueError) as error_context:
            set_job_resources(self.num_gpus, self.invalid_ram)
        
        error_message = 'Invalid RAM quantity. Please provide a RAM quantity greater than zero.'
        self.assertIn(error_message, error_context.exception.args)

    def test_ram_set_less_than_or_equal_to_zero_does_not_actually_set_job_resources(self):
        with self.assertRaises(ValueError) as error_context:
            set_job_resources(self.num_gpus, self.invalid_ram)

        job_resources = current_foundations_context().job_resources
        self.assertEqual(self.default_job_resources, job_resources)

    def test_ram_set_to_none_is_valid_configuration(self):
        set_job_resources(self.num_gpus, None)

        expected_job_resources = JobResources(num_gpus=self.num_gpus, ram=None)
        job_resources = current_foundations_context().job_resources
        self.assertEqual(expected_job_resources, job_resources)

    def test_gpu_set_to_non_integer_value_throw_value_error(self):
        with self.assertRaises(ValueError) as error_context:
            set_job_resources(self.non_integer_gpu, self.ram)
        
        error_message = 'Invalid GPU quantity. Please provide a non-negative integer GPU quantity.'
        self.assertIn(error_message, error_context.exception.args)

    def test_gpu_set_to_non_integer_value_not_actually_set_job_resources(self):
        with self.assertRaises(ValueError) as error_context:
            set_job_resources(self.non_integer_gpu, self.ram)

        job_resources = current_foundations_context().job_resources
        self.assertEqual(self.default_job_resources, job_resources)

    def test_gpu_set_to_negative_value_throw_value_error(self):
        with self.assertRaises(ValueError) as error_context:
            set_job_resources(self.negative_gpus, self.ram)
        
        error_message = 'Invalid GPU quantity. Please provide a non-negative integer GPU quantity.'
        self.assertIn(error_message, error_context.exception.args)

    def test_gpu_set_to_negative_value_not_actually_set_job_resources(self):
        with self.assertRaises(ValueError) as error_context:
            set_job_resources(self.negative_gpus, self.ram)

        job_resources = current_foundations_context().job_resources
        self.assertEqual(self.default_job_resources, job_resources)

    def test_set_job_resources_ram_defaults_to_none(self):
        set_job_resources(num_gpus=self.num_gpus)

        job_resources = current_foundations_context().job_resources
        self.assertEqual(JobResources(self.num_gpus, None), job_resources)

    def test_set_job_resources_num_gpus_defaults_to_zero(self):
        set_job_resources(ram=self.ram)
        job_resources = current_foundations_context().job_resources
        self.assertEqual(JobResources(0, self.ram), job_resources)