"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest


class TestRunJob(unittest.TestCase):

    def test_can_run_job(self):
        import acceptance.fixtures.stages as stages
        from vcat import pipeline

        stage = pipeline.stage(stages.bundle_value, 5)
        stage.persist()

        deployment = stage.run()
        deployment.wait_for_deployment_to_complete()
        result = deployment.fetch_job_results()

        self.assertEqual(result['stage_contexts']
                         [stage.uuid()]['stage_output'], 5)
