"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 10 2018
"""

import unittest

import foundations
import acceptance.fixtures.stages as stages

class TestRunJobWithUnserializableOutputs(unittest.TestCase):
    def setUp(self):
        from acceptance.cleanup import cleanup
        cleanup()

    def test_persist_generator(self):
        returns_generator = foundations.create_stage(stages.returns_generator)
        executes_generator = foundations.create_stage(stages.executes_generator)

        gen = returns_generator(55).persist()
        gen_value = executes_generator(gen)

        deployment = gen_value.run()
        deployment.wait_for_deployment_to_complete()
        result = deployment.fetch_job_results()

        self.assertEqual(result['stage_contexts']
                         [gen_value.uuid()]['stage_output'], 55)