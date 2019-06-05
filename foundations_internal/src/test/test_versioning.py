"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 10 2018
"""


from foundations_spec import *

class TestVersioning(Spec):
    
    mock_distribution = let_patch_mock('pkg_resources.get_distribution')

    @let
    def version(self):
        from foundations_internal.versioning import _foundations_version as foundations_version
        return foundations_version()

    @set_up
    def set_up(self):
        self.mock_distribution.side_effect = self.get_distribution
        self.returned_version = None

    def test_returns_not_installed_when_distribution_raises_error(self):
        self.assertEqual('no-version-installed', self.version)

    def test_returns_current_version(self):
        self.returned_version = self.faker.uuid4()
        self.assertEqual(self.returned_version, self.version)

    def get_distribution(self, library):
        from pkg_resources import DistributionNotFound

        if library != 'dessa_foundations':
            raise ValueError('Unsupported library {}'.format(library))

        if self.returned_version is None:
            raise DistributionNotFound

        mock = Mock()
        mock.version = self.returned_version
        return mock