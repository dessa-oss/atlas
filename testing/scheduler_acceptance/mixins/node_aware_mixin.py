"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class NodeAwareMixin(object):

    @classmethod
    def set_up_api(klass):
        from foundations_scheduler.kubernetes_api_wrapper import KubernetesApiWrapper

        klass._api = KubernetesApiWrapper()
        klass._core_api = klass._api.core_api()

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