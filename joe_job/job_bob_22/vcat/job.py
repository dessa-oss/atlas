class Job(object):

    def __init__(self, pipeline_connector, **kwargs):
        self.kwargs = kwargs
        self._pipeline_connector = pipeline_connector

    def run(self):
        return self._pipeline_connector.run(**self.kwargs)

    def pipeline_context(self):
        return self._pipeline_connector.pipeline_context()

    def serialize(self):
        import dill as pickle
        return pickle.dumps(self, protocol=2)

    @staticmethod
    def deserialize(serialized_self):
        import dill as pickle
        return pickle.loads(serialized_self)