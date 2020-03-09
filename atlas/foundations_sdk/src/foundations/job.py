

class Job(object):

    def __init__(self, pipeline_connector, **kwargs):
        self.kwargs = kwargs
        self._pipeline_connector = pipeline_connector

    def pipeline_context(self):
        return self._pipeline_connector.pipeline_context()

    def serialize(self):
        from foundations_internal.serializer import serialize
        return serialize(self)

    @staticmethod
    def deserialize(serialized_self):
        from foundations_internal.serializer import deserialize
        return deserialize(serialized_self)
