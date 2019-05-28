"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *
import foundations

@skip
class TestSetJobResources(Spec):

    @set_up
    def set_up(self):
        from scheduler_acceptance.cleanup import cleanup
        cleanup()

    @tear_down
    def tear_down(self):
        from foundations_contrib.global_state import current_foundations_context
        current_foundations_context().reset_job_resources()

    @set_up_class
    def set_up_class(klass):
        from foundations_scheduler.kubernetes_api_wrapper import KubernetesApiWrapper
        klass._api = KubernetesApiWrapper()
        klass._core_api = klass._api.core_api()

    def test_set_job_resources(self):
        from scheduler_acceptance.fixtures.stages import get_ram_in_gb_when_limit_set, get_number_of_gpus

        foundations.set_job_resources(1, 3)

        get_number_of_gpus = foundations.create_stage(get_number_of_gpus)
        stage_get_number_of_gpus = get_number_of_gpus()

        get_ram_in_gb = foundations.create_stage(get_ram_in_gb_when_limit_set)
        stage_get_ram_in_gb = get_ram_in_gb()

        log_metric = foundations.create_stage(self._log_resource_metrics)
        stage = log_metric(stage_get_number_of_gpus, stage_get_ram_in_gb)

        job = stage.run()
        job.wait_for_deployment_to_complete()

        metrics = foundations.get_metrics_for_all_jobs('default')
        job_metrics = metrics[metrics['job_id'] == job.job_name()]
        self.assertEqual(1, job_metrics['number_of_GPUs'].iloc[0])
        self.assertEqual(3, job_metrics['ram_in_GB'].iloc[0])

    def test_job_is_run_with_default_resources_when_resources_not_set(self):
        from scheduler_acceptance.fixtures.stages import get_ram_in_gb_when_limit_not_set, get_number_of_gpus

        get_number_of_gpus = foundations.create_stage(get_number_of_gpus)
        stage_get_number_of_gpus = get_number_of_gpus()

        get_ram_in_gb = foundations.create_stage(get_ram_in_gb_when_limit_not_set)
        stage_get_ram_in_gb = get_ram_in_gb()

        log_metric = foundations.create_stage(self._log_resource_metrics)
        stage = log_metric(stage_get_number_of_gpus, stage_get_ram_in_gb)

        job = stage.run()
        job.wait_for_deployment_to_complete()
        job_id = job.job_name()
        node_name = self._get_node_for_job(job_id)
        memory_capacity = self._get_memory_capacity_for_node(node_name)

        metrics = foundations.get_metrics_for_all_jobs('default')
        job_metrics = metrics[metrics['job_id'] == job.job_name()]
        self.assertEqual(0, job_metrics['number_of_GPUs'].iloc[0])
        self.assertEqual(memory_capacity, job_metrics['ram_in_GB'].iloc[0])

    def test_exception_thrown_when_job_is_run_with_too_many_resources(self):
        from scheduler_acceptance.fixtures.stages import get_ram_in_gb_when_limit_set, get_number_of_gpus

        foundations.set_job_resources(20, 10000)

        get_number_of_gpus = foundations.create_stage(get_number_of_gpus)
        stage_get_number_of_gpus = get_number_of_gpus()

        get_ram_in_gb = foundations.create_stage(get_ram_in_gb_when_limit_set)
        stage_get_ram_in_gb = get_ram_in_gb()

        log_metric = foundations.create_stage(self._log_resource_metrics)
        stage = log_metric(stage_get_number_of_gpus, stage_get_ram_in_gb)

        with self.assertRaises(RuntimeError) as error_context:
            stage.run()
        
        error_message = 'Could not deploy job - no node exists with sufficient resources'
        self.assertIn(error_message, error_context.exception.args)

    @staticmethod
    def _log_resource_metrics(number_of_gpus, ram_in_gb):
        foundations.log_metric('number_of_GPUs', number_of_gpus)
        foundations.log_metric('ram_in_GB', ram_in_gb)

    def _get_node_for_job(self, job_id):
        list_of_pods = self._core_api.list_namespaced_pod('foundations-scheduler-test')
        node_names = [pod.spec.node_name for pod in list_of_pods.items if self._is_foundations_job_pod(pod, job_id)]
        return node_names[0]

    def _get_memory_capacity_for_node(self, node_name):
        node = self._core_api.read_node(node_name)
        capacity_kb = node.status.capacity['memory'][:-2]
        return int(capacity_kb) / 1024 / 1024

    @staticmethod
    def _is_foundations_job_pod(pod, job_id):
        pod_name = pod.metadata.name
        return pod_name.startswith('foundations-job-{}'.format(job_id))
