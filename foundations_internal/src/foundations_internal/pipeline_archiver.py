

class PipelineArchiver(object):

    def __init__(self, pipeline_name, archive_listing, persisted_data_archive, provenance_archive, job_source_archive,
                 artifact_archive, miscellaneous_archive):
        self._archive_listing = archive_listing
        self._pipeline_name = pipeline_name
        self._persisted_data_archive = persisted_data_archive
        self._provenance_archive = provenance_archive
        self._job_source_archive = job_source_archive
        self._artifact_archive = artifact_archive
        self._miscellaneous_archive = miscellaneous_archive

    def append_persisted_data(self, name, data):
        if data is not None:
            return self._persisted_data_archive.append(name, data, self._pipeline_name)

    def append_provenance(self, provenance):
        if provenance is not None:
            return self._provenance_archive.append('provenance', provenance, self._pipeline_name)

    def append_job_source(self, source_file_path):
        if source_file_path is not None:
            return self._job_source_archive.append_file('job_source', source_file_path, self._pipeline_name,
                                                        self._pipeline_name + '.tgz')

    def append_artifact(self, name, artifact):
        if artifact is not None:
            return self._artifact_archive.append('artifacts/' + name, artifact, self._pipeline_name)

    def append_miscellaneous(self, name, data):
        if data is not None:
            return self._miscellaneous_archive.append('miscellaneous/' + name, data, self._pipeline_name)

    def append_tracker(self):
        return self._archive_listing.track_pipeline(self._pipeline_name)

    def append_persisted_file(self, target_file_path, source_file_path):
        return self._persisted_data_archive.append_file('artifacts', source_file_path, self._pipeline_name,
                                                        target_file_path)

    def pipeline_name(self):
        return self._pipeline_name

    def fetch_persisted_data(self, name):
        return self._persisted_data_archive.fetch(name, self._pipeline_name)

    def fetch_provenance(self):
        return self._provenance_archive.fetch('provenance', self._pipeline_name)

    def fetch_job_source(self, target_file_path):
        return self._job_source_archive.fetch_file_path('job_source', target_file_path, self._pipeline_name)

    def fetch_artifact(self, name):
        return self._artifact_archive.fetch('artifacts/' + name, self._pipeline_name)

    def fetch_miscellaneous(self, name):
        return self._miscellaneous_archive.fetch('miscellaneous/' + name, self._pipeline_name)

    def fetch_persisted_file(self, source_file_path, target_file_path):
        return self._persisted_data_archive.fetch_file_path_to_target_file_path('artifacts', source_file_path,
                                                                                self._pipeline_name, target_file_path)
