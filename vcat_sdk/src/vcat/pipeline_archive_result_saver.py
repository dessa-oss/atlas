class PipelineArchiveResultSaver(object):

    def __init__(self, archive):
        self._archive = archive

    def save(self, name, results):
        self._archive.append(name, results)

    def clear(self):
        pass
