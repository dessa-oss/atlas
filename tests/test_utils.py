"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

import vcat.utils as utils

class TestUtils(unittest.TestCase):
    def test_file_archive_name_no_prefix(self):
        self.assertEqual("asdf", utils.file_archive_name(None, "asdf"))

    def test_file_archive_name_with_prefix(self):
        self.assertEqual("pre/asdf", utils.file_archive_name("pre", "asdf"))

    def test_file_archive_name_add_pref_no_pref(self):
        self.assertEqual("add/asdf", utils.file_archive_name_with_additional_prefix(None, "add", "asdf"))

    def test_file_archive_name_add_pref_with_pref(self):
        self.assertEqual("pre/add/asdf", utils.file_archive_name_with_additional_prefix("pre", "add", "asdf"))

    def test_concat_strings_no_strings(self):
        self.assertEqual("", utils.concat_strings([]))

    def test_concat_strings_one_string(self):
        self.assertEqual("asdf", utils.concat_strings(["asdf"]))

    def test_concat_strings_some_strings(self):
        strings = ["madam ", "i'm ", "adam"]
        self.assertEqual("madam i'm adam", utils.concat_strings(strings))

    def test_tgz_archive_without_extension(self):
        self.assertEqual("archive", utils.tgz_archive_without_extension("archive.tgz"))

    def test_pretty_time_valid_time(self):
        import time
        import datetime

        now = time.time()

        self.assertEqual(datetime.datetime.fromtimestamp(now), utils.pretty_time(now))

    def test_pretty_time_invalid_time(self):
        self.assertEqual("asdf", utils.pretty_time("asdf"))

    def test_restructure_headers_both_empty(self):
        self.assertEqual([], utils.restructure_headers([], []))

    def test_restructure_headers_no_first_headers(self):
        all_headers = ["a", "c", "b"]
        self.assertEqual(all_headers, utils.restructure_headers(all_headers, []))

    def test_restructure_headers_no_all_headers(self):
        first_headers = ["a", "c", "b"]
        self.assertEqual([], utils.restructure_headers([], first_headers))

    def test_restructure_headers_both_headers(self):
        first_headers = ["b", "c", "a", "d"]
        all_headers = ["z", "a", "b", "c", "y"]

        self.assertEqual(["b", "c", "a", "z", "y"], utils.restructure_headers(all_headers, first_headers))

    def test_dict_like_iter_with_list(self):
        test_list = ["this", "is", "a", "test"]
        tracked_index = 0

        for key, val in utils.dict_like_iter(test_list):
            self.assertEqual(key, tracked_index)
            self.assertEqual(val, test_list[key])
            tracked_index += 1

    def test_dict_like_iter_with_dict(self):
        test_dict = {
            "key1": 0,
            "key4": 1,
            "asdf66": 90,
            "yooo": 33
        }

        for key, val in utils.dict_like_iter(test_dict):
            self.assertEqual(val, test_dict[key])

    def test_unfinished(self):
        self.fail("do the rest of the tests!")