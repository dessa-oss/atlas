"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def returns(*types):
    def _internal(function):
        return function
    return _internal


def api_resource(klass):
    print(dir(klass()))
    if hasattr(klass, 'index'):
        print('has index')
    else:
        print('no index')
    return klass


def description(description):
    def _internal(klass):
        return klass
    return _internal
