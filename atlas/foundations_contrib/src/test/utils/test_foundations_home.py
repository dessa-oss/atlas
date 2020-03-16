
from foundations_spec import *
from foundations_contrib.utils import foundations_home

class TestFoundationsHome(Spec):

    @let
    def override_home(self):
        return self.faker.uri_path()
    
    def test_foundations_home_returns_default_home(self):
        override_environment = {}
        self.patch('os.environ', override_environment)

        self.assertEqual('~/.foundations', foundations_home())

    def test_foundations_home_returns_environment_home_when_specified(self):
        override_environment = {'FOUNDATIONS_HOME': self.override_home}
        self.patch('os.environ', override_environment)

        self.assertEqual(self.override_home, foundations_home())