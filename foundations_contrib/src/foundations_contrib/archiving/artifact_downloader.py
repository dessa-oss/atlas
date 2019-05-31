"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ArtifactDownloader(object):

    def __init__(self, archiver):
        self._archiver = archiver
    
    def download_files(self, source_directory, download_directory):
        for file_path in self._artifact_file_list(source_directory):
            self._download_file(file_path, download_directory)

    def _artifact_file_list(self, source_directory):
        from fnmatch import fnmatch

        file_list = self._archiver.fetch_miscellaneous('job_artifact_listing.pkl')
        return [file_path for file_path in file_list if fnmatch(file_path, source_directory + '*')]

    def _download_file(self, file_path, download_directory):
        from os import makedirs
        from os.path import dirname

        target_path = download_directory + '/' + file_path
        print('remote file >>', file_path)
        print('target_path >>>', target_path)
        directory = dirname(target_path)
        makedirs(directory, exist_ok=True)
        self._archiver.fetch_persisted_file(file_path, target_path)
