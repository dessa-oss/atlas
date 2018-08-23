"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class FoundationsContext(object):
    """[summary]
    
    Arguments:
        pipeline {Pipeline} -- The initial Foundation pipeline to use for stages
    """
    
    def __init__(self, pipeline):
        self._pipeline = pipeline

    def pipeline(self):
        return self._pipeline

    def pipeline_context(self):
        return self._pipeline.pipeline_context()