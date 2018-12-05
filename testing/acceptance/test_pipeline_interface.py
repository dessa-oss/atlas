"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest


class TestPipelineInterface(unittest.TestCase):

    def setUp(self):
        from acceptance.cleanup import cleanup
        cleanup()

    def test_pipeline_interface(self):
        from staged_acceptance.fixtures.stages import bundle_value, add
        import acceptance.fixtures.stages as stages
        from foundations import Hyperparameter, Job
        from foundations_contrib.job_source_bundle import JobSourceBundle
        from foundations_internal import deployment_manager

        previous_stage = bundle_value(5)
        stage = add(previous_stage, Hyperparameter("b"))
        stage.persist()

        deployment = stage.run(b=4)

        deployment.wait_for_deployment_to_complete()
        result = deployment.fetch_job_results()

        self.assertEqual(result['stage_contexts']
                         [stage.uuid()]['stage_output'], 9)
