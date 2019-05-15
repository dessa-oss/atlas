"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *
from foundations_production.serving import create_job_workspace

class TestCreateJobWorkspace(Spec):

    mock_get_pipeline_archiver_for_job = let_patch_mock('foundations_contrib.archiving.get_pipeline_archiver_for_job', ConditionalReturn())
    mock_pipeline_archiver = let_mock()
    
    mock_job_source_bundle_class = let_patch_mock('foundations_contrib.job_source_bundle.JobSourceBundle', ConditionalReturn())
    mock_job_source_bundle = let_mock()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def workspace_path(self):
        return '/tmp/foundations_workspaces/' + self.job_id

    @set_up
    def set_up(self):
        self._fetch_job_source_called = False
        
        self.mock_get_pipeline_archiver_for_job.return_when(self.mock_pipeline_archiver, self.job_id)
        self.mock_job_source_bundle_class.return_when(self.mock_job_source_bundle, self.job_id, self.workspace_path)

        self.mock_pipeline_archiver.fetch_job_source.side_effect = self._set_fetch_job_source_called
        self.mock_job_source_bundle.unbundle.side_effect = self._check_fetch_job_source_called

    def test_create_job_workspace_fetches_job_source_bundle_to_workspace_directory(self):
        create_job_workspace(self.job_id)
        self.mock_pipeline_archiver.fetch_job_source.assert_called_with(self.workspace_path + '/' + self.job_id + '.tgz')

    def test_create_job_workspace_extracts_before_cleaning_up_job_source_bundle(self):
        create_job_workspace(self.job_id)
        expected_calls = [call.unbundle(self.workspace_path), call.cleanup()]
        self.assertEqual(expected_calls, self.mock_job_source_bundle.method_calls)
    
    def _set_fetch_job_source_called(self, *args):
        self._fetch_job_source_called = True
    
    def _check_fetch_job_source_called(self, *args):
        if not self._fetch_job_source_called:
            raise AssertionError('fetch_job_source should be called before unbundle')
       

    