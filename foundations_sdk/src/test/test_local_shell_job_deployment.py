"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest

from foundations.local_shell_job_deployment import LocalShellJobDeployment
from foundations.scheduler_local_backend import LocalBackend

class TestLocalShellJobDeployment(unittest.TestCase):
    def test_backend_returns_local_backend(self):
        self.assertEqual(LocalShellJobDeployment.scheduler_backend(), LocalBackend)