"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec.helpers import *

def let_fake_redis():
    @let
    def _callback(self):
        from fakeredis import FakeRedis
        redis = FakeRedis()
        redis.flushall()
        return redis
    return _callback

def get_network_adapter(name):
    import ifaddr

    for adapter in ifaddr.get_adapters():
        if adapter.name == name:
            return adapter

def get_network_address(adapter_name):
    network_adapter = get_network_adapter(adapter_name)
    
    for ip in network_adapter.ips:
        if isinstance(ip.ip, str):
            return ip.ip