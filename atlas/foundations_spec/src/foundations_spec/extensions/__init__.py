
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
    
    if network_adapter is not None:
        for ip in network_adapter.ips:
            if isinstance(ip.ip, str):
                return ip.ip

def run_process(command, directory, environment=None):
    import subprocess
    import os

    env = None
    if environment is not None:
        env = dict(os.environ)
        env.update(environment)

    previous_directory = os.getcwd()
    try:
        os.chdir(directory)
        with open('/dev/null') as null_file:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=null_file, env=env)
        out, err = process.communicate()
        return out.decode()
    finally:
        os.chdir(previous_directory)

