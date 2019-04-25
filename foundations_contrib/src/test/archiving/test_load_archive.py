"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *
from foundations_contrib.archiving import load_archive

class TestLoadArchive(Spec):

    mock_archive_instance = let_mock()
    mock_archive_constructor_args = let_mock()

    @let
    def mock_archive_type(self):
        mock_archive_klass = ConditionalReturn()
        mock_archive_klass.return_when(self.mock_archive_instance, self.mock_archive_constructor_args)
        return mock_archive_klass

    @let
    def fake_archive_name(self):
        return self.faker.word()

    @let
    def fake_archive_implementation(self):
        fake_archive_implementation_name = '{}_implementation'.format(self.fake_archive_name)

        return {
            fake_archive_implementation_name: {
                'archive_type': self.mock_archive_type,
                'constructor_arguments': [self.mock_archive_constructor_args]
            }
        }

    @let_now
    def config_manager(self):
        from foundations_contrib.config_manager import ConfigManager
        return self.patch('foundations_contrib.global_state.config_manager', ConfigManager())

    def test_returns_null_archive_when_none_is_configured(self):
        from foundations_contrib.null_archive import NullArchive

        archive_instance = load_archive(self.fake_archive_name)
        self.assertIsInstance(archive_instance, NullArchive)

    def test_returns_archive_instance_when_it_is_configured(self):
        config = self.config_manager.config()
        config.update(self.fake_archive_implementation)

        archive_instance = load_archive(self.fake_archive_name)
        self.assertIs(self.mock_archive_instance, archive_instance)