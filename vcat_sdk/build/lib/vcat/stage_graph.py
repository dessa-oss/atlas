"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.stage_connector import StageConnector


class StageGraph(object):
    def stage(self, stage):
        return StageConnector(stage, [])

    def join(self, stage, upstream_connectors):
        return StageConnector(stage, upstream_connectors)
