

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

    def test_folder_job_source_bundle_has_cleanup_method(self):
        with self.assert_does_not_raise():
            self.bundle.cleanup()

