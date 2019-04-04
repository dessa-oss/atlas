"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *

class TestGetIPAddress(Spec):

    mock_ifaddr = let_patch_mock('ifaddr.get_adapters')
    wrong_adapter = let_mock()
    right_adapter = let_mock()

    @let
    def fake_adapter_name(self):
        return self.faker.name()

    @set_up
    def set_up(self):
        self.wrong_adapter.name = 'wrong0'
        self.right_adapter.name = self.fake_adapter_name
        self.mock_ifaddr.return_value = [self.wrong_adapter, self.right_adapter]

    def test_returns_the_adapter_we_want(self):
        from foundations_spec.extensions import get_network_adapter
        self.assertEqual(self.right_adapter, get_network_adapter(self.fake_adapter_name))