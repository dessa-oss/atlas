

from foundations_spec.extensions import let_fake_redis
from foundations_spec import *


class TestProjectNoteListingController(Spec):

    mock_redis = let_fake_redis()

    @let_now
    def auth_client(self):
        constructor = self.patch(
            "foundations_rest_api.utils.AuthenticationClient",
            autospec=True,
        )
        return constructor("conf", "redirect")

    @let
    def message(self):
        return self.faker.sentence()

    @let
    def userid(self):
        return self.faker.word()

    @let
    def username(self):
        return self.faker.word()

    @let
    def controller(self):
        from foundations_rest_api.v2beta.controllers.project_note_listing_controller import (
            ProjectNoteListingController,
        )
        return ProjectNoteListingController()

    @let
    def project_name(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        self.patch("foundations_rest_api.global_state.redis_connection", self.mock_redis)
        # mock the redis used by authentication
        self.patch("foundations_contrib.global_state.redis_connection", self.mock_redis)
        self.controller.params = {
            "author": self.userid,
            "message": self.message,
            "project_name": self.project_name,
        }

    def test_post_returns_a_confirmation_message(self):
        expected_result = (
            f"Note with author: {self.userid} created with message: {self.message}"
        )
        self.assertEqual(expected_result, self.controller.post().as_json())

    def test_index_returns_empty(self):
        expected_result = []
        self.assertEqual(expected_result, self.controller.index().as_json())

    def test_post_then_index_returns_same_data(self):
        from foundations_rest_api.global_state import app_manager

        headers = {"Authorization": "bearer token"}
        self.auth_client.users_info = ConditionalReturn()
        self.auth_client.users_info.return_when({self.userid: self.username}, "token")

        with app_manager.app().test_request_context(headers=headers):
            self.controller.post()
            index_result = self.controller.index().as_json()
            self.assertEqual(1, len(index_result))
            self.assertEqual(self.message, index_result[0]["message"])
