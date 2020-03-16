


from foundations_spec import *

class TestJobTagsController(Spec):

    mock_tag_set_klass = let_patch_mock_with_conditional_return('foundations_events.producers.tag_set.TagSet')
    mock_tag_set = let_mock()
    mock_message_router = let_patch_mock('foundations_contrib.global_state.message_router')
    
    @let_now
    def redis(self):
        import fakeredis
        return self.patch('foundations_rest_api.global_state.redis_connection', fakeredis.FakeRedis())

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
        from foundations_rest_api.v2beta.controllers.job_tags_controller import JobTagsController
        return JobTagsController()

    @let
    def random_tags(self):
        result = {key: self.faker.sentence() for key in self.faker.words()}
        result[self.key] = self.value
        return result

    @set_up
    def set_up(self):
        import fakeredis
        self.patch('foundations_rest_api.global_state.redis_connection', fakeredis.FakeRedis())
        self.controller.params = {'job_id': self.job_id, 'tag': {'key': self.key, 'value': self.value}}
        self.mock_tag_set_klass.return_when(self.mock_tag_set, self.mock_message_router, self.job_id, self.key, self.value)

    def test_post_returns_a_confirmation_message(self):
        expected_result = f'Tag key: {self.key}, value: {self.value} created for job {self.job_id}'
        self.assertEqual(expected_result, self.controller.post().as_json())
