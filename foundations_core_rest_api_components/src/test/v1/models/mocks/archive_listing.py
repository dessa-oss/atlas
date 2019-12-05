"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class MockArchiveListing(object):

    def __init__(self):
        self._listing = []

    def track_pipeline(self, name):
        self._listing.append(name)

    def get_pipeline_names(self):
        return self._listing
