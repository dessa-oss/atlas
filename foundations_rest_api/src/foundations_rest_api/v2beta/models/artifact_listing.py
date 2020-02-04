"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Kyle De Freitas <k.defreitas@dessa.com>, 07 2019
"""

def artifact_listing_for_job(job_id):
    import json
    from foundations_contrib.global_state import redis_connection
    
    serialized_metadata = redis_connection.get(f'jobs:{job_id}:user_artifact_metadata')
    deserialized_metadata = json.loads(serialized_metadata) if serialized_metadata is not None else {'key_mapping': {}, 'metadata': {}}
    
    artifact_listing = list(_artifact_listing_generator(deserialized_metadata))
    artifact_listing.sort(key=lambda entry: entry[1])
    return artifact_listing

def _artifact_listing_generator(metadata):
    for key in metadata['key_mapping']:
        filename = metadata['key_mapping'][key]
        yield (key, filename, metadata['metadata'][filename])