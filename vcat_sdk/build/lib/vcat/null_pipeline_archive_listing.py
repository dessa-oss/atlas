"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class NullArchiveListing(object):

    def track_pipeline(self, pipeline_name):
        pass

    def get_pipeline_names(self):
        return []
