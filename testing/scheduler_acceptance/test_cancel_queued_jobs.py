"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

import foundations
from foundations import cancel_queued_jobs

# @skip
class TestCancelQueuedJobs(Spec):

    @set_up_class
    def set_up_class(klass):
        from foundations_scheduler.kubernetes_api_wrapper import KubernetesApiWrapper

        klass._api = KubernetesApiWrapper(context='kubernetes-admin@kubernetes')
        klass._core_api = klass._api.core_api()
        klass._custom_objects_api = klass._api.custom_objects_api()
        klass._batch_api = klass._api.batch_api()

    @set_up
    def set_up(self):
        from scheduler_acceptance.cleanup import cleanup
        cleanup()

        worker_node_ram = self._get_worker_node_ram()
        foundations.set_job_resources(0, worker_node_ram * 0.51)

    def test_cancel_no_jobs_if_job_list_is_empty(self):
        cancelled_jobs_with_status = cancel_queued_jobs([])
        self.assertEqual({}, cancelled_jobs_with_status)

    def test_cancel_fails_if_no_jobs_queued(self):
        from uuid import uuid4

        job_list = [str(uuid4()), str(uuid4()), str(uuid4())]
        expected_job_cancel_status = {job_id: False for job_id in job_list}

        self.assertEqual(expected_job_cancel_status, cancel_queued_jobs(job_list))

    def test_cancel_succeeds_if_job_queued(self):
        import foundations
        from scheduler_acceptance.fixtures.stages import wait_five_seconds, finishes_instantly

        wait_five_seconds = foundations.create_stage(wait_five_seconds)
        finishes_instantly = foundations.create_stage(finishes_instantly)

        wait_five_seconds_deployment_object = wait_five_seconds().run()

        self._wait_for_job_to_be_running(wait_five_seconds_deployment_object)

        finishes_instantly_deployment_object = finishes_instantly().run()

        job_id = finishes_instantly_deployment_object.job_name()
        expected_job_cancel_status = {job_id: True}

        self.assertEqual(expected_job_cancel_status, cancel_queued_jobs([job_id]))
        self._assert_job_does_not_exist(job_id)

    def test_cancel_fails_if_job_is_completed(self):
        import foundations

        from scheduler_acceptance.fixtures.stages import finishes_instantly

        finishes_instantly = foundations.create_stage(finishes_instantly)
        deployment_object = finishes_instantly().run()
        deployment_object.wait_for_deployment_to_complete()

        job_id = deployment_object.job_name()
        expected_job_cancel_status = {job_id: False}

        self.assertEqual(expected_job_cancel_status, cancel_queued_jobs([job_id]))
        self._assert_job_exists(job_id)

    def test_cancel_fails_if_job_is_running(self):
        import foundations
        from scheduler_acceptance.fixtures.stages import wait_five_seconds

        wait_five_seconds = foundations.create_stage(wait_five_seconds)
        deployment_object = wait_five_seconds().run()

        self._wait_for_job_to_be_running(deployment_object)

        job_id = deployment_object.job_name()
        expected_job_cancel_status = {job_id: False}

        self.assertEqual(expected_job_cancel_status, cancel_queued_jobs([job_id]))
        self._assert_job_exists(job_id)

    def _wait_for_job_to_be_running(self, deployment_object):
        import time

        from foundations_contrib.global_state import redis_connection
        from foundations.helpers.queued import list_jobs

        while deployment_object.job_name() in list_jobs(redis_connection):
            time.sleep(0.5)

    def _get_worker_node_ram(self):
        node_list = self._core_api.list_node()
        node = node_list.items[0]
        node_resources = node.status.allocatable
        ram_kb_string = self._kb_string_without_suffix(node_resources['memory'])
        ram_kb = int(ram_kb_string)
        return self._ram_kb_to_gb(ram_kb)

    def _kb_string_without_suffix(self, kb_string):
        return kb_string.replace('Ki', '')

    def _ram_kb_to_gb(self, ram_kb):
        return ram_kb / 1024 / 1024

    def _assert_job_exists(self, job_id):
        from kubernetes.client.rest import ApiException

        kubernetes_job_name = 'foundations-job-{}'.format(job_id)

        try:
            self._custom_objects_api.get_namespaced_custom_object(
                'foundations.dessa.com',
                'v1',
                'foundations-scheduler-test',
                'foundations-jobs',
                job_id
            )

            self._batch_api.read_namespaced_job(kubernetes_job_name, 'foundations-scheduler-test')
        except ApiException as ex:
            if ex.status == 404:
                raise AssertionError('job {} does not exist, but should'.format(job_id))
            raise

    def _assert_job_does_not_exist(self, job_id):
        try:
            self._assert_job_exists(job_id)
        except AssertionError:
            return

        raise AssertionError('job {} exists, but should not'.format(job_id))