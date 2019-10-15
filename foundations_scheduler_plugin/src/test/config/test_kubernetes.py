"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestKubernetes(Spec):

    def test_kubernetes_master_ip_returns_ip_address_from_kube_config(self):
        import yaml
        from foundations_scheduler_plugin.config.kubernetes import kubernetes_master_ip
 
        run_process_mock = self.patch('subprocess.check_output', ConditionalReturn())
        master_address = self.faker.ipv4_private()
        cluster_name = self.faker.name()
        context_name = self.faker.name()
        kube_config = {
            'clusters': [{
                'name': cluster_name,
                'cluster': {
                    'server': f'http://{master_address}:6443'
                }
            }],
            'contexts': [{
                'name': context_name,
                'context': {
                    'cluster': cluster_name
                }
            }],
            'current-context': context_name
        }
        run_process_mock.return_when(yaml.dump(kube_config).encode(), ['kubectl', 'config', 'view'])
 
        self.assertEqual(master_address, kubernetes_master_ip())

    def test_kubernetes_master_ip_returns_ip_address_from_kube_config(self):
        import yaml
        from foundations_scheduler_plugin.config.kubernetes import kubernetes_master_ip

        run_process_mock = self.patch('subprocess.check_output', ConditionalReturn())
        master_address = self.faker.ipv4_private()
        not_master_address = self.faker.ipv4_private()

        kube_config = {
            'apiVersion': 'v1',
            'clusters': [],
            'contexts': [],
            'current-context': '',
            'kind': 'Config',
            'preferences': {},
            'users': []
        }


        node_yaml = {
            'items': [
                {
                    'status': {
                        'addresses': [
                            {
                                'address': master_address,
                                'type': 'InternalIP'
                            },

                            {
                                'address': not_master_address,
                                'type': 'NotInternalIP'
                            }
                        ]
                    }
                }
            ]
        }

        run_process_mock.return_when(yaml.dump(kube_config).encode(), ['kubectl', 'config', 'view'])
        run_process_mock.return_when(yaml.dump(node_yaml).encode(), ['kubectl', 'get', 'no', '-o', 'yaml', '-l', 'node-role.kubernetes.io/master='])

        self.assertEqual(master_address, kubernetes_master_ip())

    @skip('Pending merge from trunk')
    def test_kubernetes_redis_url_returns_redis_endpoint_from_kubernetes_service(self):
        import yaml
        from foundations_scheduler_plugin.config.kubernetes import kubernetes_redis_url
 
        run_process_mock = self.patch('subprocess.check_output', ConditionalReturn())
        redis_ip = self.faker.ipv4_private()
        port = self.faker.random.randint(1234, 5678)
        endpoint = {
            'subsets': [{
                'addresses': [{'ip': redis_ip}],
                'ports': [{'port': port}]
            }]
        }
        run_process_mock.return_when(yaml.dump(endpoint).encode(), ['kubectl', 'get', 'endpoints', '-n', 'foundations-scheduler-test', 'redis', '-o', 'yaml'])
 
        self.assertEqual(f'redis://{redis_ip}:{port}', kubernetes_redis_url())
