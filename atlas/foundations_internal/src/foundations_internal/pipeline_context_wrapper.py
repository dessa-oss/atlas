
class PipelineContextWrapper(object):
    def __init__(self, pipeline_context):
        self._pipeline_context = pipeline_context

    def pipeline_context(self):
        return self._pipeline_context