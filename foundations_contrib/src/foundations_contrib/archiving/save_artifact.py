"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def save_artifact(filepath, key=None):
    from foundations_contrib.global_state import log_manager, current_foundations_context

    logger = log_manager.get_logger(__name__)
    foundations_context = current_foundations_context()

    if not foundations_context.is_in_running_job():
        logger.warning('Cannot save artifact outside of job.')
    else:
        job_id = foundations_context.job_id()

        artifact_saver = _ArtifactSaver(logger, filepath, job_id, key)
        artifact_saver.save_artifact()

class _ArtifactSaver(object):

    def __init__(self, logger, filepath, job_id, key):
        from foundations_contrib.archiving import load_archive

        self._logger = logger
        self._artifact_archive = load_archive('artifact_archive')
        self._filepath = filepath
        self._job_id = job_id
        self._key = key

    def save_artifact(self):
        if self._artifact_exists():
            self._logger.warning(f'Artifact "{self._blob_name_in_archive()}" already exists - overwriting.')

        self._append_artifact_to_archive()
        self._append_metadata_to_archive()

    def _artifact_exists(self):
        return self._artifact_archive.exists(f'artifacts/{self._blob_name_in_archive()}', prefix=self._job_id)

    def _append_artifact_to_archive(self):
        self._artifact_archive.append_file('artifacts', self._filepath, self._job_id, target_name=self._key)

    def _append_metadata_to_archive(self):
        metadata_blob_basename = self._blob_name_in_archive()
        self._artifact_archive.append(f'artifacts/{metadata_blob_basename}.metadata', self._metadata(), self._job_id)

    def _blob_name_in_archive(self):
        return self._key or self._filename()

    def _filename(self):
        import os.path as path
        return path.basename(self._filepath)

    def _metadata(self):
        import os.path as path

        _, extension = path.splitext(self._filepath)
        extension_without_dot = extension[1:]
        return {'file_extension': extension_without_dot}