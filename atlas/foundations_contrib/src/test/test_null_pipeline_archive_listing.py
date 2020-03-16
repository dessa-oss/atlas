
import unittest
from foundations_contrib.null_pipeline_archive_listing import NullPipelineArchiveListing


class TestNullPipelineArchiveListing(unittest.TestCase):

    def test_has_track_pipeline_interface(self):
        listing = NullPipelineArchiveListing()
        try:
            listing.track_pipeline('some_pipeline')
        except:
            self.fail(
                "#some_pipeline was not defined as a function taking a single parameter")

    def test_get_pipeline_names_returns_empty(self):
        listing = NullPipelineArchiveListing()
        self.assertEqual([], listing.get_pipeline_names())
