"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest


class TestDuplicateJobSource(unittest.TestCase):

    def setUp(self):
        from acceptance.cleanup import cleanup
        cleanup()

    def test_can_duplicate_job_source(self):
        import acceptance.fixtures.stages as stages
        from acceptance.config import TEST_UUID
        from vcat import pipeline, JobPersister, ResultReader

        stage = pipeline.stage(stages.bundle_value, 5)
        stage.persist()

        deployment = stage.run()
        deployment.wait_for_deployment_to_complete()

        with JobPersister.load_archiver_fetch() as archiver:
            reader = ResultReader(archiver)
            duplicate_path = 'tmp/duplicate_jobs_{}'.format(TEST_UUID)
            reader.create_working_copy(deployment.job_name(), duplicate_path)

            with open(__file__, 'r') as file:
                expected_content = file.read()

            with open('{}/acceptance/test_duplicate_job_source.py'.format(duplicate_path), 'r') as file:
                result_content = file.read()

            self.assertEqual(expected_content, result_content)
