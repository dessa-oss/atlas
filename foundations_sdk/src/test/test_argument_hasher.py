"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.argument_hasher import ArgumentHasher

class TestArgumentHasher(unittest.TestCase):
    def test_constant_empty_list_arg(self):
        arg_hash = ArgumentHasher([[]], {}).make_hash()
        self.assertEqual(arg_hash, "10a34637ad661d98ba3344717656fcc76209c2f8")

    def test_constant_singleton_list_arg(self):
        arg_hash = ArgumentHasher([[1]], {}).make_hash()
        self.assertEqual(arg_hash, "715e4a633a340a9c4c1f8c53399d05c0f3a434b6")

    def test_constant_multi_element_list_arg(self):
        arg_hash = ArgumentHasher([["hello", "world", "breh"]], {}).make_hash()
        self.assertEqual(arg_hash, "30f7b967800ec86e8149792ea349ea84266e6b5e")
