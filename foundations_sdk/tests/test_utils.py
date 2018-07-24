"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

import foundations.utils as utils

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

    def test_dict_like_append_with_list(self):
        test_list = ["asdf", "fdas"]
        utils.dict_like_append(test_list, None, "dfd")
        utils.dict_like_append(test_list, None, "fdas")

        self.assertEqual(test_list, ["asdf", "fdas", "dfd", "fdas"])

    def test_dict_like_append_with_dict(self):
        test_dict = {
            "asdf": 0,
            "fdsa": 1
        }

        utils.dict_like_append(test_dict, "dfd", 33)
        utils.dict_like_append(test_dict, "fdsa", 100)

        result_dict = {
            "asdf": 0,
            "fdsa": 100,
            "dfd": 33
        }

        self.assertEqual(test_dict, result_dict)

    def test_split_process_output_zero_length(self):
        lazy_output = utils.split_process_output(b"")
        self.assertEqual([], list(lazy_output))

    def test_split_process_output_few_lines(self):
        lazy_output = utils.split_process_output(b"      This\nis\na\ntest  ")
        self.assertEqual([u"This", u"is", u"a", u"test"], list(lazy_output))

    def test_force_encoding_utf_8(self):
        string_utf_8 = u"asdf"
        bytes_string = utils.force_encoding(string_utf_8)

        self.assertTrue(isinstance(bytes_string, bytes))
        self.assertEqual(b"asdf", bytes_string)

    def test_force_encoding_bytes(self):
        string_unicode = u"asdf"
        bytes_string = utils.force_encoding(string_unicode)

        self.assertTrue(isinstance(bytes_string, bytes))
        self.assertEqual(string_unicode, bytes_string.decode('utf-8'))

    def test_is_string(self):
        from sys import version_info

        string_unicode = u"asdf"
        string_bytes = b"asdf"
        not_a_string = 1234

        self.assertTrue(utils.is_string(string_unicode))
        self.assertFalse(utils.is_string(not_a_string))

        bytes_is_string = utils.is_string(string_bytes)

        if version_info[0] < 3:
            self.assertTrue(bytes_is_string)
        else:
            self.assertFalse(bytes_is_string)

    def test_take_one_element_from_empty_generator(self):
        from foundations_sdk_fixtures.utils_fixtures import create_empty_generator

        empty_gen = utils.take_from_generator(1, create_empty_generator())

        for _ in empty_gen:
            self.fail("should not be any values in an empty generator")

    def test_take_nothing_from_generator(self):
        from foundations_sdk_fixtures.utils_fixtures import create_generator

        empty_gen = utils.take_from_generator(0, create_generator())

        for _ in empty_gen:
            self.fail("should not be any values in an empty generator")

    def test_take_one_element_from_generator(self):
        from foundations_sdk_fixtures.utils_fixtures import create_generator

        one_elem_gen = utils.take_from_generator(1, create_generator())

        elems = []
        for item in one_elem_gen:
            elems.append(item)

        self.assertEqual([0], elems)

    def test_take_two_elements_from_generator(self):
        from foundations_sdk_fixtures.utils_fixtures import create_generator

        two_elem_gen = utils.take_from_generator(2, create_generator())

        elems = []
        for item in two_elem_gen:
            elems.append(item)

        self.assertEqual([0, 1], elems)

    def test_take_too_many_elements_from_generator(self):
        from foundations_sdk_fixtures.utils_fixtures import create_generator

        ten_elem_gen = utils.take_from_generator(10000, create_generator())

        elems = []
        for item in ten_elem_gen:
            elems.append(item)

        self.assertEqual(list(range(10)), elems)

    def test_take_from_generator_lazy_generation(self):
        from foundations_sdk_fixtures.utils_fixtures import create_effectful_generator

        # should throw an exception if take_from_generator does not create a generator (lazy list)
        ten_elem_gen = utils.take_from_generator(10, create_effectful_generator())

        # take only the first item
        elems = [next(ten_elem_gen)]

        self.assertEqual([0], elems)