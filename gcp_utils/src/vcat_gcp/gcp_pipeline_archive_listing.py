"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class GCPPipelineArchiveListing(object):

    def __init__(self, bucket):
        from vcat_gcp.gcp_bucket import GCPBucket
        from vcat.prefixed_bucket import PrefixedBucket
        from vcat.bucket_pipeline_listing import BucketPipelineListing

        self._listing = BucketPipelineListing(
            PrefixedBucket, 'pipeline_archives', GCPBucket, bucket)

    def track_pipeline(self, pipeline_name):
        return self._listing.track_pipeline(pipeline_name)

    def get_pipeline_names(self):
        return self._listing.get_pipeline_names()
