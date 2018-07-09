"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

import vcat_sdk_fixtures.stage_connector_wrapper_fixtures as scf
import vcat_sdk_helpers.stage_connector_wrapper_helpers as sch

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

        all_results = sch.get_results_list(deployments)
        self.assertEqual([{'a': 1}], all_results)

    def test_random_search_simple_params_dict_two_iterations(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.random_search(scf.simple_param_set, max_iterations=2)

        self.assertEqual(len(deployments), 2)

        all_results = sch.get_results_list(deployments)
        self.assertEqual([{'a': 1}] * 2, all_results)

    def test_random_search_less_simple_param_set_two_iterations(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.random_search(scf.less_simple_param_set, max_iterations=2)

        self.assertEqual(len(deployments), 2)

        for result in sch.get_results_list(deployments):
            self.assertIn(result['a'], [1, 2])

    def test_random_search_more_complex_param_set_twenty_iterations(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.random_search(scf.params_ranges_dict, max_iterations=20)

        self.assertEqual(len(deployments), 20)

        for result in sch.get_results_list(deployments):
            self.assertIn(result['param_0'], [1, 2])
            self.assertIn(result['param_1'], [3])
            self.assertIn(result['param_2'], [4, 5, 6, 7])

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

        all_results = sch.get_results_list(deployments)
        self.assertEqual([{'a': 1}], all_results)

    def test_grid_search_simple_params_dict_two_iterations(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.grid_search(scf.simple_param_set, max_iterations=2)

        self.assertEqual(len(deployments), 1) # will not do same hyperparam set twice

        all_results = sch.get_results_list(deployments)
        self.assertEqual([{'a': 1}], all_results)

    def test_grid_search_less_simple_param_set_two_iterations(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.grid_search(scf.less_simple_param_set, max_iterations=2)

        self.assertEqual(len(deployments), 2)

        all_results = sch.get_sorted_results_items_list(deployments)
        self.assertEqual([[('a', 1)], [('a', 2)]], all_results)

    def test_grid_search_less_simple_param_set_ten_iterations(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.grid_search(scf.less_simple_param_set, max_iterations=10)

        self.assertEqual(len(deployments), 2)

        all_results = sch.get_sorted_results_items_list(deployments)
        self.assertEqual([[('a', 1)], [('a', 2)]], all_results)

    def test_grid_search_less_simple_param_set_one_iteration(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.grid_search(scf.less_simple_param_set, max_iterations=1)

        self.assertEqual(len(deployments), 1)

        all_results = sch.get_sorted_results_items_list(deployments)
        self.assertEqual([[('a', 1)]], all_results)

    def test_grid_search_more_complex_param_set_all_iterations(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.grid_search(scf.params_ranges_dict)

        self.assertEqual(len(deployments), 8)

        expected_results = sch.params_cart_prod([1, 2], [3], [4, 5, 6, 7])
        expected_results.sort()

        all_results = sch.get_sorted_results_items_list(deployments)
        self.assertEqual(expected_results, all_results)

    def test_grid_search_more_complex_param_set_five_out_of_eight_iterations(self):
        from vcat.deployment_utils import extract_results

        dummy_pipeline = scf.make_dummy_pipeline()
        deployments = dummy_pipeline.grid_search(scf.params_ranges_dict, max_iterations=5)

        self.assertEqual(len(deployments), 5)

        all_results = sch.get_sorted_results_items_list(deployments)

        expected_results = sch.params_cart_prod([1, 2], [3], [4, 5, 6, 7])

        expected_results = expected_results[0:5]
        expected_results.sort()

        self.assertEqual(expected_results, all_results)

    # def test_adaptive_search_