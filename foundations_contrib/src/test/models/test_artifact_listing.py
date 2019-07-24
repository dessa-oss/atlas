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
        return ConditionalReturn()

    @let
    def mock_listing(self):
        return self.faker.sentences()
    
    @set_up
    def setup(self):
        self.mock_archive.list_files = ConditionalReturn()
        self.mock_archive.list_files.return_when(self.mock_listing, '*', self.job_id)

    def test_artifact_listing_for_job(self):
        from foundations_contrib.models.artifact_listing import artifact_listing_for_job
        mock_listing = artifact_listing_for_job(self.job_id, self.mock_archive)
        self.assertEqual(self.mock_listing, mock_listing)

