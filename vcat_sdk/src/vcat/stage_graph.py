from vcat.stage_connector import StageConnector


class StageGraph(object):
    def stage(self, stage):
        return StageConnector(stage, [])

    def join(self, stage, upstream_connectors):
        return StageConnector(stage, upstream_connectors)
