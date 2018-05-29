class PipelineArchiver(object):

    def __init__(self, stage_log_archive, persisted_data_archive, provenance_archive, job_source_archive, artifact_archive, miscellanous_archive):
        self._stage_log_archive = stage_log_archive
        self._persisted_data_archive = persisted_data_archive
        self._provenance_archive = provenance_archive
        self._job_source_archive = job_source_archive
        self._artifact_archive = artifact_archive
        self._miscellanous_archive = miscellanous_archive

    def append_stage_log(self, stage_uuid_string, log):
        return self._stage_log_archive.append(stage_uuid_string + '/stage_log', log)

    def append_persisted_data(self, name, data):
        return self._persisted_data_archive.append(name, data)

    def append_provenance(self, provenance):
        return self._provenance_archive.append('provenance', provenance)

    def append_job_source(self, source):
        return self._job_source_archive.append('job_source', source)

    def append_artifact(self, name, artifact):
        return self._artifact_archive.append(name, artifact)

    def append_miscellanous(self, name, data):
        return self._miscellanous_archive.append(name, data)
