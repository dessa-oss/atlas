import requests
import subprocess
from foundations_spec import *

from typing import List
import time

class TestCanPingService(Spec):
    
    @set_up
    def set_up(self):
        result = _run_command(['sh', 'integration/fixtures/spin_up_kubernetes_service.sh'])
        
    @tear_down
    def tear_down(self):
        result = _run_command(['sh', 'integration/fixtures/tear_down_kubernetes_service.sh'])
    
    def test_can_ping_pod_running_within_different_service_using_query_job_pod(self):
        result = _run_command(['integration/fixtures/get_service_ip.sh'])
        ip_addr = result.stdout.decode().strip()
        time.sleep(2)
        self.assertEqual('{"message":"Hello"}',requests.get(f'http://{ip_addr}').text.strip())


def _run_command(command: List[str]) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60, check=True)
    except subprocess.TimeoutExpired as error:
        print('Command timed out.')
        print(error.stdout.decode())
        raise Exception(error.stderr.decode())
    except subprocess.CalledProcessError as error:
        print(f'Command failed: \n\t{" ".join(command)}\n')
        raise Exception(error.stderr.decode())
    return result
