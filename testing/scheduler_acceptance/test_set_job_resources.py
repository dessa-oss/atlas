"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *
import foundations
from scheduler_acceptance.mixins.node_aware_mixin import NodeAwareMixin

class TestSetJobResources(Spec, NodeAwareMixin):

    @set_up_class
    def set_up_class(klass):
        klass.set_up_api()

    @set_up
    def set_up(self):
        from scheduler_acceptance.cleanup import cleanup
        cleanup()

    @tear_down
    def tear_down(self):
        foundations.set_job_resources(0, None)

    def test_set_job_resources(self):
        from scheduler_acceptance.fixtures.stages import get_ram_in_gb_when_limit_set, get_number_of_gpus

        foundations.set_job_resources(0, 3)

        get_number_of_gpus = foundations.create_stage(get_number_of_gpus)
        stage_get_number_of_gpus = get_number_of_gpus()

        get_ram_in_gb = foundations.create_stage(get_ram_in_gb_when_limit_set)
        stage_get_ram_in_gb = get_ram_in_gb()

        log_metric = foundations.create_stage(_log_resource_metrics)
        stage = log_metric(stage_get_number_of_gpus, stage_get_ram_in_gb)

        job = stage.run()
        job.wait_for_deployment_to_complete()

        metrics = foundations.get_metrics_for_all_jobs('default')
        job_metrics = metrics[metrics['job_id'] == job.job_name()]
        self.assertEqual(0, job_metrics['number_of_GPUs'].iloc[0])
        self.assertEqual(3, job_metrics['ram_in_GB'].iloc[0])

    def test_job_is_run_with_default_resources_when_resources_not_set(self):
        from scheduler_acceptance.fixtures.stages import get_ram_in_gb_when_limit_not_set, get_number_of_gpus
        from foundations_contrib.global_state import current_foundations_context

        current_foundations_context().reset_job_resources()

        get_number_of_gpus = foundations.create_stage(get_number_of_gpus)
        stage_get_number_of_gpus = get_number_of_gpus()

        get_ram_in_gb = foundations.create_stage(get_ram_in_gb_when_limit_not_set)
        stage_get_ram_in_gb = get_ram_in_gb()

        log_metric = foundations.create_stage(_log_resource_metrics)
        stage = log_metric(stage_get_number_of_gpus, stage_get_ram_in_gb)

        job = stage.run()
        job.wait_for_deployment_to_complete()
        job_id = job.job_name()
        node_name = self._get_node_for_job(job_id)
        memory_capacity = self._get_memory_capacity_for_node(node_name)

        metrics = foundations.get_metrics_for_all_jobs('default')
        job_metrics = metrics[metrics['job_id'] == job.job_name()]
        ram_available_to_job = job_metrics['ram_in_GB'].iloc[0]

        ram_error = abs(memory_capacity - ram_available_to_job) / memory_capacity

        self.assertEqual(1, job_metrics['number_of_GPUs'].iloc[0])
        self.assertLess(ram_error, 0.01)

    def test_exception_thrown_when_job_is_run_with_too_many_resources(self):
        from scheduler_acceptance.fixtures.stages import get_ram_in_gb_when_limit_set, get_number_of_gpus

        foundations.set_job_resources(20, 10000)

        get_number_of_gpus = foundations.create_stage(get_number_of_gpus)
        stage_get_number_of_gpus = get_number_of_gpus()

        get_ram_in_gb = foundations.create_stage(get_ram_in_gb_when_limit_set)
        stage_get_ram_in_gb = get_ram_in_gb()

        log_metric = foundations.create_stage(_log_resource_metrics)
        stage = log_metric(stage_get_number_of_gpus, stage_get_ram_in_gb)

        with self.assertRaises(RuntimeError) as error_context:
            stage.run()
        
        error_message = 'Could not deploy job - no node exists with sufficient resources'
        self.assertIn(error_message, error_context.exception.args)

def _log_resource_metrics(number_of_gpus, ram_in_gb):
    foundations.log_metric('number_of_GPUs', number_of_gpus)
    foundations.log_metric('ram_in_GB', ram_in_gb)