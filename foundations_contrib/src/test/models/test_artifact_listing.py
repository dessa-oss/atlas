"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Kyle De Freitas <k.defreitas@dessa.com>, 08 2019
"""

from foundations_spec import *

import json
from foundations_contrib.models.artifact_listing import artifact_listing_for_job

class TestArtifactListing(Spec):

    @let
    def job_id(self):
        return self.faker.uuid4()

    @set_up
    def set_up(self):
        from fakeredis import FakeRedis

        self._redis = self.patch('foundations_contrib.global_state.redis_connection', FakeRedis())

    @tear_down
    def tear_down(self):
        self._redis.flushall()

    def test_artifact_listing_returns_empty_dict_if_no_artifact_metadata_in_redis(self):
        self.assertEqual([], artifact_listing_for_job(self.job_id))

    def test_artifact_listing_returns_metadata_for_artifact_if_it_exists(self):
        key = self.faker.word()
        artifact_name = self.faker.word()

        artifact_metadata = self._artifact_metadata()
        metadata_in_redis = {
            'key_mapping': {
                key: artifact_name
            },
            'metadata': {
                artifact_name: artifact_metadata
            }
        }

        self._redis.set(f'jobs:{self.job_id}:user_artifact_metadata', json.dumps(metadata_in_redis))

        self.assertEqual([(key, artifact_name, artifact_metadata)], artifact_listing_for_job(self.job_id))

    def test_artifact_listing_returns_metadata_for_all_existing_artifacts(self):
        artifact_name_0 = self.faker.word()
        artifact_name_1 = self.faker.word()
        artifact_name_2 = self.faker.word()

        artifact_metadata_0 = self._artifact_metadata()
        artifact_metadata_1 = self._artifact_metadata()
        artifact_metadata_2 = self._artifact_metadata()

        metadata_in_redis = {
            'key_mapping': {
                artifact_name_1: 'filename_1',
                artifact_name_0: 'filename_0',
                artifact_name_2: 'filename_2'
            },
            'metadata': {
                'filename_0': artifact_metadata_0,
                'filename_1': artifact_metadata_1,
                'filename_2': artifact_metadata_2
            }
        }

        self._redis.set(f'jobs:{self.job_id}:user_artifact_metadata', json.dumps(metadata_in_redis))

        expected_metadata = [
            (artifact_name_0, 'filename_0', artifact_metadata_0),
            (artifact_name_1, 'filename_1', artifact_metadata_1),
            (artifact_name_2, 'filename_2', artifact_metadata_2)
        ]

        self.assertEqual(expected_metadata, artifact_listing_for_job(self.job_id))

    def _artifact_metadata(self):
        return {self.faker.word(): self.faker.word()}