"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock
from foundations_spec import *

class TestRunStagelessJob(Spec):

    class FakeJob(object):

        def run(self):
            raise AssertionError('Old style job executed')

    def test_stageless_script_run_when_enabled_stages_is_false(self):
        import os
        import subprocess
        import sys
        from importlib import import_module
        from io import StringIO
        from foundations_contrib.resources.main import run_job_variant
        
        os.environ['enable_stages'] = 'False'
        os.environ['script_to_run'] = 'integration/fixtures/user_stageless_script.py'

        cwd = os.getcwd()
        os.chdir('integration/fixtures')

        try:
            sys.stdout = captured_io = StringIO()
            run_job_variant(self.FakeJob())
            self.assertEqual(captured_io.getvalue(), 'Hello from stageless script\n')
        finally:
            os.chdir(cwd)