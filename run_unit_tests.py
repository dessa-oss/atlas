"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

def create_test_suite(module_dir_name):
    loader = unittest.TestLoader()
    return loader.discover(module_dir_name + '/tests', pattern='test_*.py')

def run_tests_from(module_dir_name):
    runner = unittest.TextTestRunner()
    runner.run(create_test_suite(module_dir_name))

if __name__ == '__main__':
    run_tests_from('foundations_sdk')
    run_tests_from('gcp_utils')
    run_tests_from('ssh_utils')