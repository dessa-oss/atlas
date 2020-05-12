from foundations_internal.provenance import Provenance

class FoundationsContext(object):
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
                pipeline_context = FoundationsContext.Pipeline.PipelineContext()
            self._pipeline_context = pipeline_context

        def pipeline_context(self):
            return self._pipeline_context

    """The global state for all staging related functionality for Foundations.
    This is where everything awesome begins!!!

    Arguments:
        pipeline {Pipeline} -- The initial Foundation pipeline to use for stages
    """

    def __init__(self, pipeline=None):
        if pipeline is None:
            pipeline = FoundationsContext.Pipeline()
        self._pipeline = pipeline
        self._job_resources = self._default_job_resources()

    def __getstate__(self):
        raise ValueError('FoundationsContexts do not support serialization')

    def __setstate__(self, state):
        raise ValueError('FoundationsContexts do not support serialization')

    @property
    def project_name(self):
        return self.provenance.project_name

    @project_name.setter
    def project_name(self, project_name):
        self.provenance.project_name = project_name


    @property
    def job_id(self):
        return self._pipeline.pipeline_context().file_name

    @job_id.setter
    def job_id(self, value):
        self._pipeline.pipeline_context().file_name = value

    @property
    def job_resources(self):
        return self._job_resources

    @job_resources.setter
    def job_resources(self, job_resources):
        self._job_resources = job_resources

    def reset_job_resources(self):
        self._job_resources = self._default_job_resources()

    def is_in_running_job(self):
        try:
            return self._pipeline.pipeline_context().file_name is not None
        except ValueError:
            return False

    @property
    def provenance(self):
        return self._pipeline.pipeline_context().provenance

    def _default_job_resources(self):
        from foundations_internal.job_resources import JobResources
        return JobResources(1, None)

    @property
    def user_name(self):
        return self._pipeline.pipeline_context().provenance.user_name

    @user_name.setter
    def user_name(self, value):
        self._pipeline.pipeline_context().provenance.user_name = value