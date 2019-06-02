"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestPipelineArchiver(Spec):

    persisted_archive = let_mock()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def source_file_name(self):
        return self.faker.uri_path()

    @let
    def target_file_name(self):
        return self.faker.uri_path()

    @let
    def pipeline_archiver(self):
        from foundations_internal.pipeline_archiver import PipelineArchiver
        return PipelineArchiver(self.job_id, None, None, self.persisted_archive, None, None, None, None)

    def test_append_persisted_file_uploads_specified_file(self):
        self.pipeline_archiver.append_persisted_file(self.target_file_name, self.source_file_name)
        self.persisted_archive.append_file.assert_called_with('artifacts', self.source_file_name, self.job_id, self.target_file_name)

    def test_fetch_persisted_file_downloads_specified_file(self):
        self.pipeline_archiver.fetch_persisted_file(self.source_file_name, self.target_file_name)
        self.persisted_archive.fetch_file_path_to_target_file_path.assert_called_with('artifacts', self.source_file_name, self.job_id, self.target_file_name)
