"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class RowCountChecker(object):

    def __init__(self, reference_row_count):
        self._number_of_rows = reference_row_count

    def validate(self, row_count_to_check):
        return abs(row_count_to_check - self._number_of_rows) / self._number_of_rows