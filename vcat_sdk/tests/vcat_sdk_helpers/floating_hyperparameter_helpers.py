"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def make_unique_and_sorted(list_to_uniquify):
    set_from_list = set(list_to_uniquify)
    to_sort = list(set_from_list)
    to_sort.sort()
    return to_sort