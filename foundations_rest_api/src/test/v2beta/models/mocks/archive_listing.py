
class MockArchiveListing(object):

    def __init__(self):
        self._listing = []

    def track_pipeline(self, name):
        self._listing.append(name)

    def get_pipeline_names(self):
        return self._listing
