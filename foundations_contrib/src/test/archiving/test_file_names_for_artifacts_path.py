"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *
from foundations_contrib.archiving.file_names_for_artifacts_path import file_names_for_artifacts_path

class TestFileNamesForArtifactsPath(Spec):

    def test_yields_no_value(self):
        empty_walk = []
        file_paths = list(file_names_for_artifacts_path(empty_walk))
        self.assertEqual([], file_paths)

    def test_yields_single_file(self):
        single_file_walk = [('dir1', None, ['file'])]
        file_paths = list(file_names_for_artifacts_path(single_file_walk))
        self.assertEqual(['dir1/file'], file_paths)
    
    def test_yields_multiple_files_in_same_directory(self):
        multiple_file_walk = [('dir1', None, ['file2', 'file3'])]
        file_paths = list(file_names_for_artifacts_path(multiple_file_walk))
        self.assertEqual(['dir1/file2', 'dir1/file3'], file_paths)
    
    def test_yields_multiple_files_across_multiple_directories(self):
        multiple_file_walk = [('other_dir', None, ['file2']), ('other_dir2', None, ['file3'])]
        file_paths = list(file_names_for_artifacts_path(multiple_file_walk))
        self.assertEqual(['other_dir/file2', 'other_dir2/file3'], file_paths)        

    def test_properly_joins_paths(self):
        single_file_walk = [('dir1', None, ['/file'])]
        file_paths = list(file_names_for_artifacts_path(single_file_walk))
        self.assertEqual(['/file'], file_paths)