"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

import vcat_sdk_fixtures.stage_connector_wrapper_fixtures as scf

class TestStageConnectorWrapper(unittest.TestCase):
    def test_random_search_empty_params_dict_zero_iterations(self):
        dummy_pipeline = scf.make_dummy_pipeline()
        self.assertEqual({}, dummy_pipeline.random_search({}, max_iterations=0))

    def test_random_search_non_empty_params_dict_zero_iterations(self):
        dummy_pipeline = scf.make_dummy_pipeline()
        self.assertEqual({}, dummy_pipeline.random_search(scf.params_ranges_dict, max_iterations=0))

    def test_random_search_empty_params_dict_one_iteration(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.random_search({}, max_iterations=1)

        self.assertEqual(len(deployments), 1)

        for _, deployment in deployments.items():
            results = deployment.fetch_job_results()
            results = extract_results(results)
            self.assertEqual({}, results)

    def test_random_search_simple_params_dict_one_iteration(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.random_search(scf.simple_param_set, max_iterations=1)

        self.assertEqual(len(deployments), 1)

        for _, deployment in deployments.items():
            results = deployment.fetch_job_results()
            results = extract_results(results)
            self.assertEqual({'a': 1}, results)

    def test_random_search_simple_params_dict_two_iterations(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.random_search(scf.simple_param_set, max_iterations=2)

        self.assertEqual(len(deployments), 2)

        for _, deployment in deployments.items():
            results = deployment.fetch_job_results()
            results = extract_results(results)
            self.assertEqual({'a': 1}, results)

    def test_random_search_less_simple_param_set_two_iterations(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.random_search(scf.less_simple_param_set, max_iterations=2)

        self.assertEqual(len(deployments), 2)

        for _, deployment in deployments.items():
            results = deployment.fetch_job_results()
            results = extract_results(results)
            self.assertIn(results['a'], [1, 2])

    def test_random_search_more_complex_param_set_twenty_iterations(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.random_search(scf.params_ranges_dict, max_iterations=20)

        self.assertEqual(len(deployments), 20)

        for _, deployment in deployments.items():
            results = deployment.fetch_job_results()
            results = extract_results(results)
            self.assertIn(results['param_0'], [1, 2])
            self.assertIn(results['param_1'], [3])
            self.assertIn(results['param_2'], [4, 5, 6, 7])

    def test_grid_search_empty_params_dict_zero_iterations(self):
        dummy_pipeline = scf.make_dummy_pipeline()
        self.assertEqual({}, dummy_pipeline.grid_search({}, max_iterations=0))

    def test_grid_search_empty_params_dict_no_max_iterations(self):
        dummy_pipeline = scf.make_dummy_pipeline()
        self.assertEqual({}, dummy_pipeline.grid_search({}))

    def test_grid_search_simple_params_dict_zero_iterations(self):
        dummy_pipeline = scf.make_dummy_pipeline()
        self.assertEqual({}, dummy_pipeline.grid_search(scf.simple_param_set, max_iterations=0))

    def test_grid_search_simple_params_dict_one_iteration(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.grid_search(scf.simple_param_set, max_iterations=1)

        self.assertEqual(len(deployments), 1)

        for _, deployment in deployments.items():
            results = deployment.fetch_job_results()
            results = extract_results(results)
            self.assertEqual({'a': 1}, results)

    def test_grid_search_simple_params_dict_two_iterations(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.grid_search(scf.simple_param_set, max_iterations=2)

        self.assertEqual(len(deployments), 1) # will not do same hyperparam set twice

        for _, deployment in deployments.items():
            results = deployment.fetch_job_results()
            results = extract_results(results)
            self.assertEqual({'a': 1}, results)

    def test_grid_search_less_simple_param_set_two_iterations(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.grid_search(scf.less_simple_param_set, max_iterations=2)

        self.assertEqual(len(deployments), 2)

        all_results = []

        for _, deployment in deployments.items():
            results = deployment.fetch_job_results()
            results = extract_results(results)
            all_results.append(list(results.items()))

        all_results.sort()

        self.assertEqual([[('a', 1)], [('a', 2)]], all_results)

    def test_grid_search_less_simple_param_set_ten_iterations(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.grid_search(scf.less_simple_param_set, max_iterations=10)

        self.assertEqual(len(deployments), 2)

        all_results = []

        for _, deployment in deployments.items():
            results = deployment.fetch_job_results()
            results = extract_results(results)
            all_results.append(list(results.items()))

        all_results.sort()

        self.assertEqual([[('a', 1)], [('a', 2)]], all_results)

    def test_grid_search_less_simple_param_set_one_iteration(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.grid_search(scf.less_simple_param_set, max_iterations=1)

        self.assertEqual(len(deployments), 1)

        all_results = []

        for _, deployment in deployments.items():
            results = deployment.fetch_job_results()
            results = extract_results(results)
            all_results.append(list(results.items()))

        all_results.sort()

        self.assertEqual([[('a', 1)]], all_results)

    def test_grid_search_more_complex_param_set_all_iterations(self):
        from vcat.deployment_utils import extract_results

        def p_items(p0, p1, p2):
            return [
                ('param_0', p0),
                ('param_1', p1),
                ('param_2', p2)
            ]

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.grid_search(scf.params_ranges_dict)

        self.assertEqual(len(deployments), 8)

        all_results = []

        for _, deployment in deployments.items():
            results = deployment.fetch_job_results()
            results = extract_results(results)
            results = list(results.items())
            results.sort()
            all_results.append(results)

        all_results.sort()

        expected_results = []

        for param_0 in [1, 2]:
            for param_1 in [3]:
                for param_2 in [4, 5, 6, 7]:
                    expected_results.append(p_items(param_0, param_1, param_2))
                    
        expected_results.sort()

        self.assertEqual(expected_results, all_results)

    def test_grid_search_more_complex_param_set_five_out_of_eight_iterations(self):
        from vcat.deployment_utils import extract_results

        def p_items(p0, p1, p2):
            return [
                ('param_0', p0),
                ('param_1', p1),
                ('param_2', p2)
            ]

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.grid_search(scf.params_ranges_dict, max_iterations=5)

        self.assertEqual(len(deployments), 5)

        all_results = []

        for _, deployment in deployments.items():
            results = deployment.fetch_job_results()
            results = extract_results(results)
            results = list(results.items())
            results.sort()
            all_results.append(results)

        all_results.sort()

        expected_results = []

        for param_0 in [1, 2]:
            for param_1 in [3]:
                for param_2 in [4, 5, 6, 7]:
                    expected_results.append(p_items(param_0, param_1, param_2))

        expected_results = expected_results[0:5]
        expected_results.sort()

        self.assertEqual(expected_results, all_results)