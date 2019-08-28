"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec.extensions import let_fake_redis
from foundations_spec import *

from foundations_rest_api.v2beta.controllers.job_tags_controller import JobTagsController

class TestJobTagsController(Spec):

    mock_redis = let_fake_redis()
    mock_tag_set_klass = let_patch_mock_with_conditional_return('foundations_contrib.producers.tag_set.TagSet')
    mock_tag_set = let_mock()
    mock_message_router = let_patch_mock('foundations_contrib.global_state.message_router')

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def key(self):
        return self.faker.word()

    @let
    def value(self):
        return self.faker.sentence()

    @let
    def controller(self):
        return JobTagsController()

    @let
    def random_tags(self):
        result = {key: self.faker.sentence() for key in self.faker.words()}
        result[self.key] = self.value
        return result

    @set_up
    def set_up(self):
        self.patch('foundations_contrib.global_state.redis_connection', self.mock_redis)
        self.controller.params = {'job_id': self.job_id, 'tag': {'key': self.key, 'value': self.value}}
        self.mock_tag_set_klass.return_when(self.mock_tag_set, self.mock_message_router, self.job_id, self.key, self.value)

    def test_create_adds_a_new_tag_to_an_existing_job(self):
        self.controller.create()
        self.mock_tag_set.push_message.assert_called()

    def test_create_returns_a_confirmation_message(self):
        expected_result = f'Tag key: {self.key}, value: {self.value} created for job {self.job_id}'
        self.assertEqual(expected_result, self.controller.create().as_json())

    def test_delete_removes_an_existing_tag_from_the_job(self):
        job_annotations_key = f'jobs:{self.job_id}:annotations'
        self.mock_redis.hmset(job_annotations_key, self.random_tags)
        self.controller.delete()
        self.assertNotIn(self.key.encode(), self.mock_redis.hgetall(job_annotations_key))

    def test_delete_returns_a_confirmation_message(self):
        expected_result = f'Tag key: {self.key} deleted from job {self.job_id}'
        self.assertEqual(expected_result, self.controller.delete().as_json())
