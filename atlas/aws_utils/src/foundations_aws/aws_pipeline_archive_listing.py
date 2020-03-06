

class AWSPipelineArchiveListing(object):

    def __init__(self, bucket):
        from foundations_aws.aws_bucket import AWSBucket
        from foundations.prefixed_bucket import PrefixedBucket
        from foundations_contrib.bucket_pipeline_listing import BucketPipelineListing

        self._listing = BucketPipelineListing(
            PrefixedBucket, 'pipeline_archives', AWSBucket, bucket)

    def track_pipeline(self, pipeline_name):
        return self._listing.track_pipeline(pipeline_name)

    def get_pipeline_names(self):
        return self._listing.get_pipeline_names()
