from foundations_internal.provenance import Provenance

class Pipeline(object):
    class PipelineContext(object):

        def __init__(self):
            self._file_name = None
            self.provenance = Provenance()

        @property
        def file_name(self):
            if not self._file_name:
                raise ValueError('Job ID is currently undefined, please set before retrieving')
            return self._file_name

        @file_name.setter
        def file_name(self, value):
            self._file_name = value

        @property
        def job_id(self):
            return self.file_name

    def __init__(self, pipeline_context=None):
        if pipeline_context is None:
            pipeline_context = Pipeline.PipelineContext()
        self._pipeline_context = pipeline_context
        self._uuid = 'eecbbe4788acaee0393bcad40f37f134566ad8a7'

    def pipeline_context(self):
        return self._pipeline_context

    def uuid(self):
        return self._uuid

    def run(self, **filler_kwargs):
        return None

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def persist(self):
        pass
