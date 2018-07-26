"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.null_pipeline_archive_listing import NullPipelineArchiveListing


class TestNullPipelineArchiveListing(unittest.TestCase):

    def test_has_track_pipeline_interface(self):
        listing = NullPipelineArchiveListing()
        try:
            listing.track_pipeline('some_pipeline')
        except:
            self.fail("#some_pipeline was not defined as a function taking a single parameter")

    def test_get_pipeline_names_returns_empty(self):
        listing = NullPipelineArchiveListing()
        self.assertEqual([], listing.get_pipeline_names())
