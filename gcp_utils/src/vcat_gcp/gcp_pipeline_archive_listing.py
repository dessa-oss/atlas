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

        self._gcp_bucket = PrefixedBucket(
            'pipeline_archives', GCPBucket, bucket)

    def track_pipeline(self, pipeline_name):
        self._gcp_bucket.upload_from_string(
            pipeline_name + '.tracker', pipeline_name)

    def get_pipeline_names(self):
        file_paths = self._gcp_bucket.list_files('*.tracker')

        return [self._gcp_bucket.download_as_string(path) for path in file_paths]
