
from foundations_rest_api.v2beta.controllers.tensorboard_controller import (
    TensorboardController,
)
from foundations_spec import *


class TestTensorboardController(Spec):

    mock_request_post = let_patch_mock("requests.post")
    mock_environ = let_patch_mock('os.environ', {})

    @let
    def api_host_name(self):
        return f"http://{self.faker.word()}:32766"

    @let
    def host_name(self):
        return f"http://{self.faker.word()}:32767"

    @let
    def controller(self):
        return TensorboardController()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def params(self):
        return {"job_ids": [self.job_id]}

    @let
    def transformed_params(self):
        return {
            "tensorboard_locations": [
                {
                    "job_id": self.job_id,
                    "synced_directory": f"archive/{self.job_id}/synced_directories/__tensorboard__",
                }
            ]
        }

    @set_up
    def set_up(self):
        self.controller.params = self.params
        self.mock_environ["TENSORBOARD_API_HOST"] = self.api_host_name
        self.mock_environ["TENSORBOARD_HOST"] = self.host_name

    def test_tensorboard_controller_post_posts_to_the_tensorboard_api_server_with_transformed_params(
        self,
    ):
        self.controller.post()
        self.mock_request_post.assert_called_with(
            f"{self.api_host_name}/create_sym_links", json=self.transformed_params
        )

    def test_tensorboard_controller_post_returns_host_url(self):
        self.controller.post()
        self.assertEqual({"url": f"{self.host_name}"}, self.controller.post().as_json())
