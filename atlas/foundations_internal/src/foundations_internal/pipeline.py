from .pipeline_context import PipelineContext

class Pipeline(object):

    def __init__(self, pipeline_context=None):
        if pipeline_context is None:
            pipeline_context = PipelineContext()
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
