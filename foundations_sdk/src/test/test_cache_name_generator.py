"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations.cache_name_generator import CacheNameGenerator


class TestCacheNameGenerator(unittest.TestCase):

    class MockLiveArgument(object):

        def __init__(self, hash):
            self._hash = hash

        def hash(self):
            return self._hash

    class MockVersion(object):

        def __init__(self, major):
            self.major = major

    @patch('sys.version_info', MockVersion(4))
    def test_hash_contains_uuid_code_python_version_and_arguments(self):
        from foundations.stage import Stage

        uuid = 'some uuid'
        stage = Stage(None, uuid, None, None)
        generator = CacheNameGenerator(stage, ())
        self.assertEqual(
            '8b9b39f50c6424377eecd107d66086751b40cc74', generator.hash())

    @patch('sys.version_info', MockVersion(3))
    def test_hash_contains_uuid_code_python_version_and_arguments_different_version(self):
        from foundations.stage import Stage

        uuid = 'some uuid'
        stage = Stage(None, uuid, None, None)
        generator = CacheNameGenerator(stage, ())
        self.assertEqual(
            '6bbe865851bc74298ad8bbae0113745a618eb27f', generator.hash())

    @patch('sys.version_info', MockVersion(3))
    def test_hash_contains_uuid_code_python_version_and_arguments_different_uuid(self):
        from foundations.stage import Stage

        uuid = 'some different uuid'
        stage = Stage(None, uuid, None, None)
        generator = CacheNameGenerator(stage, ())
        self.assertEqual(
            'fa7d3bb37675cc2388eb118a2b1c0d893d5e586a', generator.hash())

    @patch('sys.version_info', MockVersion(3))
    def test_hash_contains_uuid_code_python_version_and_arguments_different_arguments(self):
        from foundations.stage import Stage

        uuid = 'some different uuid'
        stage = Stage(None, uuid, None, None)
        argument = self.MockLiveArgument('some hash')
        generator = CacheNameGenerator(stage, (argument,))
        self.assertEqual(
            '989f291a9f07c7ae663764a53674993030f46612', generator.hash())

    @patch('sys.version_info', MockVersion(3))
    def test_hash_contains_uuid_code_python_version_and_arguments_multiple_arguments(self):
        from foundations.stage import Stage

        uuid = 'some different uuid'
        stage = Stage(None, uuid, None, None)
        argument = self.MockLiveArgument('some hash')
        argument_two = self.MockLiveArgument('some other hash')
        generator = CacheNameGenerator(stage, (argument, argument_two))
        self.assertEqual(
            'b529202746147dd927797989458a84cde8d32461', generator.hash())
