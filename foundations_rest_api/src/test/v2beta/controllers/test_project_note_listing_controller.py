"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec.extensions import let_fake_redis
from foundations_spec import *

from foundations_rest_api.v2beta.controllers.project_note_listing_controller import ProjectNoteListingController

class TestProjectNoteListingController(Spec):

    mock_redis = let_fake_redis()

    @let
    def _mock_message(self):
        return self.faker.sentence()

    @let
    def _mock_author(self):
        return self.faker.word()

    @let
    def controller(self):
        return ProjectNoteListingController()
    
    @let
    def _mock_project_name(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        self.patch('foundations_contrib.global_state.redis_connection', self.mock_redis)
        self.controller.params = {'author': self._mock_author, 'message': self._mock_message, 'project_name': self._mock_project_name}

    def test_post_returns_a_confirmation_message(self):
        expected_result = f'Note with author: {self.controller._author()} created with message: {self._mock_message}'
        self.assertEqual(expected_result, self.controller.post().as_json())
    
    def test_index_returns_empty(self):
        expected_result = []
        self.assertEqual(expected_result, self.controller.index().as_json())
    
    def test_post_then_index_returns_same_data(self):
        self.controller.post()
        index_result = self.controller.index().as_json()
        self.assertEqual(1, len(index_result))
        self.assertEqual(self._mock_message, index_result[0]['message'])
