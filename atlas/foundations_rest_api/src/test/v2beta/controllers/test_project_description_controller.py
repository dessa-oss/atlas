

from foundations_spec.extensions import let_fake_redis
from foundations_spec import *

from foundations_rest_api.v2beta.controllers.project_description_controller import ProjectDescriptionController

class TestProjectDescriptionController(Spec):

    mock_redis = let_fake_redis()

    @let
    def project_name(self):
        return self.faker.name()

    @let
    def description(self):
        return self.faker.paragraph()

    @let
    def controller(self):
        return ProjectDescriptionController()

    @set_up
    def set_up(self):
        self.patch('foundations_rest_api.global_state.redis_connection', self.mock_redis)
        self.controller.params = {'project_name': self.project_name, 'project_description': self.description}

    def test_get_returns_empty_project_description_when_none_specified(self):
        self.assertEqual({'project_description': ''}, self.controller.show().as_json())

    def test_get_returns_project_description_when_specified(self):
        self.mock_redis.set(f'projects:{self.project_name}:description', self.description)
        self.assertEqual({'project_description': self.description}, self.controller.show().as_json())

    def test_update_changes_the_description(self):
        self.controller.update().evaluate()
        description = self.mock_redis.get(f'projects:{self.project_name}:description').decode()
        self.assertEqual(self.description, description)

    def test_update_returns_a_success_message(self):
        self.controller.update()
        self.assertEqual(f'Updated description for {self.project_name}', self.controller.update().as_json())
