"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.provenance import Provenance


class TestProvenance(unittest.TestCase):

    def test_fill_python_version_has_correct_system_values(self):
        import sys

        provenance = Provenance()
        provenance_python_version = {
            "major": sys.version_info.major,
            "minor": sys.version_info.minor,
            "micro": sys.version_info.micro,
            "releaselevel": sys.version_info.releaselevel,
            "serial": sys.version_info.serial,
        }
        provenance.fill_python_version()

        self.assertEqual(provenance.python_version, provenance_python_version)

    def test_fill_python_version_with_wrong_value(self):
        import sys

        provenance = Provenance()
        provenance_python_version = {
            "major": sys.version_info.major,
            "minor": sys.version_info.minor,
            "micro": sys.version_info.micro,
            "releaselevel": sys.version_info.releaselevel,
            "serial": 'hello',
        }
        provenance.fill_python_version()

        self.assertNotEqual(provenance.python_version, provenance_python_version)
        

