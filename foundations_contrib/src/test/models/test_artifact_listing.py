"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Kyle De Freitas <k.defreitas@dessa.com>, 08 2019
"""

from foundations_spec import *


class TestArtifactListing(Spec):
    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def mock_archive(self):
        return Mock()

    @let
    def mock_listing(self):
        return [self.faker.uri_path() for _ in range(self.uri_count)]

    @let
    def uri_count(self):
        return self.faker.random.randint(2, 5)

    @let
    def archive_files(self):
        return [f'{self.job_id}/user_artifacts/{filepath}' for filepath in self.mock_listing]

    @let
    def metadata_files(self):
        return [f'{filepath}.metadata' for filepath in self.archive_files]

    @let
    def metadata_map(self):
        return {metadata_file: f'metadata blob for {metadata_file}' for metadata_file in self.metadata_files}

    @let
    def archive_listing(self):
        return self.archive_files + self.metadata_files

    @let
    def expected_artifact_listing(self):
        def _strip_prefix(filepath):
            num_to_remove = len(f'{self.job_id}/user_artifacts/')
            return filepath[num_to_remove:]

        expected_result = [(_strip_prefix(filepath), f'metadata blob for {filepath}.metadata') for filepath in self.archive_files]
        expected_result.sort(key=lambda entry: entry[0])
        return expected_result

    mock_load_archive = let_patch_mock_with_conditional_return('foundations_contrib.archiving.load_archive')

    @set_up
    def setup(self):
        self.mock_archive.list_files = ConditionalReturn()
        self.mock_archive.list_files.return_when(
            self.archive_listing, 'user_artifacts/*', self.job_id)

        self.mock_archive.fetch = ConditionalReturn()

        for filepath in self.mock_listing:
            self.mock_archive.fetch.return_when(f'metadata blob for {self.job_id}/user_artifacts/{filepath}.metadata', f'user_artifacts/{filepath}.metadata', self.job_id)

        self.mock_load_archive.return_when(self.mock_archive, 'artifact_archive')

    def test_artifact_listing_for_job_in_archive(self):
        from foundations_contrib.models.artifact_listing import artifact_listing_for_job_in_archive

        result_listing = artifact_listing_for_job_in_archive(
            self.job_id, self.mock_archive)
        self.assertEqual(self.expected_artifact_listing, result_listing)

    def test_artifact_listing_for_job_returns_list_of_artifacts(self):
        from foundations_contrib.models.artifact_listing import artifact_listing_for_job

        mock_artifact_listing = self.patch('foundations_contrib.models.artifact_listing.artifact_listing_for_job_in_archive', ConditionalReturn())
        mock_artifact_listing.return_when(self.expected_artifact_listing, self.job_id, self.mock_archive)

        result_listing = artifact_listing_for_job(self.job_id)
        self.assertEqual(self.expected_artifact_listing, result_listing)
