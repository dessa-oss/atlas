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
        capacity_kb = self._kb_memory_for_node(node)
        return self._kb_to_gb(capacity_kb)

    def _get_memory_capacity_for_largest_node(self):
        list_of_nodes = self._core_api.list_node()
        memory_capacities = map(self._kb_memory_for_node, list_of_nodes.items)
        return self._kb_to_gb(max(memory_capacities))
        
    @staticmethod
    def _kb_memory_for_node(node):
        capacity_kb = node.status.allocatable['memory'][:-2]
        return int(capacity_kb)

    @staticmethod
    def _is_foundations_job_pod(pod, job_id):
        pod_name = pod.metadata.name
        return pod_name.startswith('foundations-job-{}'.format(job_id))

    @staticmethod
    def _kb_to_gb(kb_memory):
        return kb_memory / 1024 / 1024