from foundations_internal.provenance import Provenance

class FoundationsContext(object):
    """The global state for all staging related functionality for Foundations.
    This is where everything awesome begins!!!

    Arguments:
        pipeline {Pipeline} -- The initial Foundation pipeline to use for stages
    """

    def __init__(self):
        self._job_resources = self._default_job_resources()
        self._job_id = None
        self._provenance = Provenance()

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
        if not self._job_id:
            raise ValueError('Job ID is currently undefined, please set before retrieving')
        return self._job_id

    @job_id.setter
    def job_id(self, job_id):
        self._job_id = job_id

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
            return self.job_id is not None
        except ValueError:
            return False

    @property
    def provenance(self):
        return self._provenance

    def _default_job_resources(self):
        from foundations_internal.job_resources import JobResources
        return JobResources(1, None)

    @property
    def user_name(self):
        return self.provenance.user_name

    @user_name.setter
    def user_name(self, value):
        self.provenance.user_name = value