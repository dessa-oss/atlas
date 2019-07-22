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
        from foundations_contrib.simple_tempfile import SimpleTempfile
        import os

        gcp_bucket = self._gcp_bucket(bucket_name)
        archive_bucket = self.artifact_bucket()

        list_of_backup_files = list(archive_bucket.list_files('**/*'))

        for file_name in list_of_backup_files:
            print(file_name)
            if '/venv' in file_name or '/foundations' in file_name:
                continue

            with SimpleTempfile('w+b') as tempfile:
                archive_bucket.download_to_file(file_name, tempfile)
                tempfile.flush()
                with open(tempfile.path, 'r') as file:
                    gcp_bucket.upload_from_file(f'{client_directory}/archive/{file_name}', file)
    
    def artifact_bucket(self):
        from os.path import expanduser
        from foundations_contrib.global_state import config_manager

        artifact_implementation = config_manager['artifact_archive_implementation']
        archive = artifact_implementation['archive_type'](*artifact_implementation['constructor_arguments'])
        return archive._archive._bucket

    @staticmethod
    def _gcp_bucket(bucket_name):
        return GCPBucket(bucket_name)