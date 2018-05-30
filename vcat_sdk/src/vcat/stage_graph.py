from vcat.stage_connector import StageConnector


class StageGraph(object):
    def stage(self, cache, stage):
        return StageConnector(cache, stage, [])

    def join(self, cache, stage, upstream_connectors):
        return StageConnector(cache, stage, upstream_connectors)
