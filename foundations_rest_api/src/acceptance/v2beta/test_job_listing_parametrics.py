

import foundations
from acceptance.api_acceptance_test_case_base import APIAcceptanceTestCaseBase
from acceptance.v2beta.jobs_tests_helper_mixin_v2 import JobsTestsHelperMixinV2
from foundations_spec import *


class TestJobListingParametrics(
    JobsTestsHelperMixinV2, APIAcceptanceTestCaseBase, Spec
):
    url = "/api/v2beta/projects/{_project_name}/job_listing"
    sorting_columns = []
    filtering_columns = []

    @classmethod
    def setUpClass(klass):
        JobsTestsHelperMixinV2.setUpClass()
        klass._set_project_name("hanna")

    @classmethod
    def tearDownClass(klass):
        from foundations_contrib.global_state import redis_connection as redis

        redis.flushall()

    @set_up
    def set_up(self):
        from foundations_contrib.global_state import redis_connection

        redis_connection.flushall()
        self.submit_job()

    def submit_job(self):
        import subprocess

        submit_result = subprocess.run(
            "python -m foundations submit --project-name {0} {1} {2} {3}".format(
                "hanna",
                "scheduler",
                "acceptance/v2beta/fixtures/log_metric_log_param_set_tag",
                "log_metric_log_param_set_tag.py"
            ),
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
        data = super(TestJobListingParametrics, self).test_get_route()

        job_data = data["jobs"][0]

        expected_output_metrics = [{"name": "key", "type": "string", "value": "value"}]

        for key in [
            "artifacts",
            "completed_time",
            "creation_time",
            "duration",
            "job_id",
            "start_time",
        ]:
            self.assertIn(key, job_data)
            self.assertIsNotNone(job_data[key])

        self.assertEqual(expected_output_metrics, job_data["output_metrics"])
        self.assertEqual("hanna", job_data["project"])
        self.assertEqual("completed", job_data["status"])
        self.assertEqual({"key": "value"}, job_data["tags"])

        self.assertEqual(
            [{"name": "key", "type": "string"}], data["output_metric_names"]
        )
        self.assertEqual("hanna", data["name"])
