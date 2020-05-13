
import json

def save_artifact(filepath, key=None):
    from foundations_contrib.global_state import log_manager, current_foundations_job

    logger = log_manager.get_logger(__name__)
    foundations_context = current_foundations_job()

    if not foundations_context.is_in_running_job():
        logger.warning('Cannot save artifact outside of job.')
    else:
        job_id = foundations_context.job_id

        artifact_saver = _ArtifactSaver(logger, filepath, job_id, key)
        artifact_saver.save_artifact()

class _ArtifactSaver(object):

    def __init__(self, logger, filepath, job_id, key):
        from foundations_contrib.global_state import redis_connection
        from foundations_contrib.archiving import load_archive

        self._logger = logger
        self._artifact_archive = load_archive('artifact_archive')
        self._filepath = filepath
        self._job_id = job_id
        self._key = key
        self._redis = redis_connection

    def save_artifact(self):
        existing_metadata = self._existing_metadata()

        if self._artifact_exists(existing_metadata):
            self._logger.warning(f'Artifact "{self._key_in_metadata()}" already exists - overwriting.')

        self._append_artifact_to_archive()
        self._add_metadata_to_redis(existing_metadata)

    def _artifact_exists(self, existing_metadata):
        return self._key_in_metadata() in existing_metadata['key_mapping']

    def _append_artifact_to_archive(self):
        self._artifact_archive.append_file('user_artifacts', self._filepath, self._job_id, target_name=None)

    def _key_in_metadata(self):
        return self._key or self._filename()

    def _filename(self):
        import os.path as path
        return path.basename(self._filepath)

    def _artifact_metadata(self):
        return {}

    def _add_metadata_to_redis(self, existing_metadata):
        key_in_metadata = self._key_in_metadata()
        filename = self._filename()

        if self._artifact_exists(existing_metadata):
            old_filename = existing_metadata['key_mapping'][key_in_metadata]
            existing_metadata['metadata'].pop(old_filename)

        existing_metadata['key_mapping'][key_in_metadata] = filename
        existing_metadata['metadata'][filename] = {}

        self._write_metadata(existing_metadata)

    def _existing_metadata(self):
        existing_metadata = self._redis.get(f'jobs:{self._job_id}:user_artifact_metadata')
        return json.loads(existing_metadata) if existing_metadata is not None else {'key_mapping': {}, 'metadata': {}}

    def _write_metadata(self, metadata):
        self._redis.set(f'jobs:{self._job_id}:user_artifact_metadata', json.dumps(metadata))