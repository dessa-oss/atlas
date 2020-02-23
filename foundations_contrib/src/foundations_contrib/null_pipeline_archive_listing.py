

class NullPipelineArchiveListing(object):

    def track_pipeline(self, pipeline_name):
        pass

    def get_pipeline_names(self):
        return []


class NullArchiveListing(NullPipelineArchiveListing):
    pass
