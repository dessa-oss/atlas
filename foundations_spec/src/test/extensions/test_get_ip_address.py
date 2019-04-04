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
    ipv4_object = let_mock()
    ipv6_object = let_mock()

    @let
    def fake_adapter_name(self):
        return self.faker.name()
    
    @let
    def fake_ip_address(self):
        return self.faker.ipv4()

    @set_up
    def set_up(self):
        self.wrong_adapter.name = 'wrong0'
        self.right_adapter.name = self.fake_adapter_name
        self.ipv4_object.ip = self.fake_ip_address
        self.right_adapter.ips = [self.ipv6_object, self.ipv4_object]
        self.mock_ifaddr.return_value = [self.wrong_adapter, self.right_adapter]

    def test_get_network_adapter_returns_the_adapter_we_want(self):
        from foundations_spec.extensions import get_network_adapter
        self.assertEqual(self.right_adapter, get_network_adapter(self.fake_adapter_name))
    
    def test_get_network_address_returns_correct_ip_address(self):
        from foundations_spec.extensions import get_network_address
        self.assertEqual(self.fake_ip_address, get_network_address(self.fake_adapter_name))