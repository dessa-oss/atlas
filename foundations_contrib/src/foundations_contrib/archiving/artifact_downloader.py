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
        from os import makedirs
        from os.path import dirname

        file_list = self._archiver.fetch_miscellaneous('job_artifact_listing.pkl')

        for file_path in file_list:
            target_path = download_directory + '/' + file_path
            directory = dirname(target_path)
            makedirs(directory, exist_ok=True)
            self._archiver.fetch_persisted_file(file_path, target_path)

        