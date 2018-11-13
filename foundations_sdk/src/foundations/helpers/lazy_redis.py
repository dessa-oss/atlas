"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class LazyRedis(object):
    """
    Class that lazily evaluates a callback method. Callback method should make a redis object. 

    Arguments:
        callback {function} - Function that returns an object 
    """

    def __init__(self, callback):
        self._redis_connection = None
        self._callback = callback

    def __getattr__(self, name):
        """
        If it exists, get an attribute 'name' from the return object of the callback function

        Arguments:
            name {string} -- Name of attribute 
        """
        conn = self._redis()
        inner_attribute = getattr(conn, name)
        if inner_attribute:
            return inner_attribute

        raise AttributeError(self._missing_attribute_message(name))

    def _redis(self):
        if self._redis_connection is None:
            self._redis_connection = self._make_redis()
        return self._redis_connection

    def _make_redis(self):
        return self._callback()

    def _missing_attribute_message(self, name):
        return "'{}' object has no attribute '{}'".format(self._klass.__name__, name)
