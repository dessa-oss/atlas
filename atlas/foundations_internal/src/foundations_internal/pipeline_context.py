
from foundations_internal.provenance import Provenance


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
