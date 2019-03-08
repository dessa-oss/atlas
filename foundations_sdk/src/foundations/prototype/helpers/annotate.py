"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def job_annotations(redis, job_id):
    encoded_annotations = _encoded_job_annotations(redis, job_id)
    return _decode_job_annotations(encoded_annotations)

def annotations_for_multiple_jobs(redis, list_of_job_ids):
    futures = _job_annotation_futures(redis, list_of_job_ids)
    return {job_id: future.get() for job_id, future in futures.items()}

def _job_annotation_futures(redis, list_of_job_ids):
    from foundations_contrib.redis_pipeline_wrapper import RedisPipelineWrapper
    from promise import Promise
    
    pipeline = RedisPipelineWrapper(redis.pipeline())
    encoded_futures = _multiple_encoded_job_annotations(pipeline, list_of_job_ids)
    futures = _decode_job_annotation_futures(encoded_futures)
    pipeline.execute()

    return futures

def _decode_job_annotation_futures(encoded_futures):
    return {job_id: annotations_future.then(_decode_job_annotations) for job_id, annotations_future in encoded_futures.items()}

def _multiple_encoded_job_annotations(pipeline, list_of_job_ids):
    return {job_id: _encoded_job_annotations(pipeline, job_id) for job_id in list_of_job_ids}

def _decode_job_annotations(encoded_annotations):
    return {key.decode(): value.decode() for key, value in encoded_annotations.items()}
    
def _encoded_job_annotations(redis, job_id):
    key = 'jobs:{}:annotations'.format(job_id)
    return redis.hgetall(key)
