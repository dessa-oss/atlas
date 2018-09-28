"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest

from foundations_ssh.sftp_job_deployment import SFTPJobDeployment

class TestSFTPJobDeployment(unittest.TestCase):
    def test_scheduler_backend(self):
        from foundations_ssh.default_legacy_backend import default_legacy_backend
        self.assertEqual(SFTPJobDeployment.scheduler_backend(), default_legacy_backend)