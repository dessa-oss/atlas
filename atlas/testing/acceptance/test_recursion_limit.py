
import unittest
from mock import Mock

from foundations.utils import using_python_2


@unittest.skip('Removal of this is pending on the removal of all stage related features')
class TestRecursionLimit(unittest.TestCase):

    def setUp(self):
        from acceptance.cleanup import cleanup
        cleanup()

    @unittest.skipIf(using_python_2(), 'skipping due to running python 2')
    def test_recursion_limit_can_be_overridden(self):
        import foundations
        from foundations.job import Job
        from foundations.global_state import deployment_manager

        @foundations.create_stage
        def callback(data):
            return data+1

        stage = callback(0)
        for _ in range(21):
            stage = callback(stage)

        job = Job(stage)
        config = {'recursion_limit': 10000}
        deployment_manager.deploy(config, 'test_job', job)
