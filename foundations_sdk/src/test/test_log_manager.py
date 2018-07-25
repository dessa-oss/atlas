"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.log_manager import LogManager


class TestLogManager(unittest.TestCase):

    def test_get_logger_if_string_value(self):
        log_manager = LogManager()
        logging = log_manager.get_logger('test once').info('Adding current directory to source bundle')
        # self.assertEqual(None , logging)
        # print(logging)

    # def test_get_logger_if_none_value(self):
    #     log_manager = LogManager()
    #     logging = log_manager.get_logger(None).info('None')
    #     self.assertEqual(None , logging)