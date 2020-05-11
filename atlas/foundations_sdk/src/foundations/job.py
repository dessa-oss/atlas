

class Job(object):

    def __init__(self, pipeline_connector, **kwargs):
        self.kwargs = kwargs
        self._pipeline_context = pipeline_connector.pipeline_context()

    def serialize(self):
        from foundations_internal.serializer import serialize
        return serialize(self)

    @property
    def user_name(self):
        return self._pipeline_context.provenance.user_name

    @user_name.setter
    def user_name(self, value):
        self._pipeline_context.provenance.user_name = value

    @property
    def project_name(self):
        return self._pipeline_context.provenance.project_name

    @project_name.setter
    def project_name(self, value):
        self._pipeline_context.provenance.project_name = value

    @staticmethod
    def deserialize(serialized_self):
        from foundations_internal.serializer import deserialize
        return deserialize(serialized_self)
