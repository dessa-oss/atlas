

from foundations_spec import *

class TestEmptyJob(Spec):

    def test_serialize_returns_empty_binary_data(self):
        from foundations_contrib.job_bundling.empty_job import EmptyJob
        self.assertEqual(b'', EmptyJob().serialize())
