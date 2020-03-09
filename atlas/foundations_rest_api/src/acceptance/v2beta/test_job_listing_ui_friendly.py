
from acceptance.v2beta.jobs_tests_helper_mixin_v2 import JobsTestsHelperMixinV2
from acceptance.api_acceptance_test_case_base import APIAcceptanceTestCaseBase
from foundations_spec import *

class TestJobsListingUIFriendly(JobsTestsHelperMixinV2, APIAcceptanceTestCaseBase, Spec):
    url = '/api/v2beta/projects/{_project_name}/job_listing'
    sorting_columns = []
    filtering_columns = []
    tags = {'this_tag': 'this_value', 'that_tag': 'that_value'}

    @classmethod
    def setUpClass(klass):
        JobsTestsHelperMixinV2.setUpClass()
        klass._set_project_name('lou')

    @classmethod
    def tearDownClass(klass):
        from foundations_contrib.global_state import redis_connection as redis
        redis.flushall()

    @set_up
    def set_up(self):
        from foundations_contrib.global_state import redis_connection
        redis_connection.flushall()

    def submit_job(self):
        import subprocess

        submit_result = subprocess.run(
            "python -m foundations submit --project-name lou scheduler acceptance/v2beta/fixtures/log_metric_set_tag log_metric_set_tag.py",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            assert submit_result.returncode == 0
        except AssertionError:
            output = submit_result.stdout.decode() or submit_result.stderr.decode()
            self.fail(output)

    def test_get_route(self):
        self.submit_job()

        data = super(TestJobsListingUIFriendly, self).test_get_route()
        job_data = data['jobs'][0]

        self.assertEqual(job_data['output_metrics'][0]['name'], 'hello')
        self.assertEqual(job_data['output_metrics'][0]['value'], 20)
        self.assertEqual(job_data['output_metrics'][0]['type'], 'number')
        self.assertEqual(self.tags, job_data['tags'])