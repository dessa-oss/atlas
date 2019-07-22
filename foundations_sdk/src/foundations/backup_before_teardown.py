"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan David <s.davis@dessa.com>, 06 2018
"""

from foundations_gcp.gcp_bucket import GCPBucket

class BackupBeforeTeardown(object):

    def upload_to_gcp(self, client_directory, bucket_name):
        from foundations_contrib.global_state import config_manager
        import os
        from foundations_internal.change_directory import ChangeDirectory

        bucket = self._gcp_bucket(bucket_name)

        with ChangeDirectory(self._artifact_path()):
            list_of_backup_files = self._list_of_files_to_upload()

            for file_name in list_of_backup_files:
                if '/venv' in file_name or '/foundations' in file_name:
                    continue

                with open(file_name, 'rb') as file:
                    bucket.upload_from_file(f'{client_directory}/archive/{file_name[2:]}', file) 
    
    def _list_of_files_to_upload(self):
        from foundations_contrib.archiving.file_names_for_artifacts_path import file_names_for_artifacts_path
        from os import walk

        artifact_path_crawl = walk('.')
        return list(file_names_for_artifacts_path(artifact_path_crawl))

    def _artifact_path(self):
        from os.path import expanduser
        from foundations_contrib.global_state import config_manager

        archive_path = config_manager['artifact_archive_implementation']['constructor_arguments'][0]
        return expanduser(archive_path)

    @staticmethod
    def _gcp_bucket(bucket_name):
        return GCPBucket(bucket_name)