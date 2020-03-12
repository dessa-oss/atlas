
import foundations
from acceptance.api_acceptance_test_case_base import APIAcceptanceTestCaseBase
from acceptance.v2beta.jobs_tests_helper_mixin_v2 import JobsTestsHelperMixinV2
from foundations_spec import *


class TestJobListingTrimCharacters(
    JobsTestsHelperMixinV2, APIAcceptanceTestCaseBase, Spec
):
    url = "/api/v2beta/projects/{_project_name}/job_listing"
    sorting_columns = []
    filtering_columns = []

    @classmethod
    def setUpClass(klass):
        JobsTestsHelperMixinV2.setUpClass()
        klass._set_project_name(JobsTestsHelperMixinV2._str_random_uuid())

    def submit_job(self):
        import subprocess

        submit_result = subprocess.run(
            f"python -m foundations submit --project-name {self._project_name} scheduler acceptance/v2beta/fixtures/log_int_metric log_int_metric.py",
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

        data = super(TestJobListingTrimCharacters, self).test_get_route()
        self.assertEqual(data["jobs"][0]["output_metrics"][0]["value"], "5" * 100)
