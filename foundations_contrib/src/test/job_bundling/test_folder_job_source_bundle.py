"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *

class TestFolderJobSourceBundle(Spec):

    @let
    def bundle(self):
        from foundations_contrib.job_bundling.folder_job_source_bundle import FolderJobSourceBundle
        return FolderJobSourceBundle()
        
    def test_folder_job_source_bundle_job_archive_returns_cwd(self):
        job_archive = self.bundle.job_archive()
        self.assertEqual('.', job_archive)

    def test_folder_job_source_bundle_has_bundle_method(self):
        with self.assert_does_not_raise():
            self.bundle.bundle()

