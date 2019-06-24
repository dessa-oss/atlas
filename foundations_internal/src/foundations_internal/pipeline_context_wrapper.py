"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class PipelineContextWrapper(object):
    def __init__(self, pipeline_context):
        self._pipeline_context = pipeline_context
        
    def pipeline_context(self):
        return self._pipeline_context