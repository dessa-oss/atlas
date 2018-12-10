"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Katherine Bancroft <k.bancroft@dessa.com>, 11 2018
"""


class RedisPipelineWrapper(object):
    """
    Class that creates a Redis pipeline calls can be appended to. 
    """

    def __init__(self, redis_pipeline):
        self._pipe = redis_pipeline
        self._futures = []

    def execute(self):
        """
        Executes Redis pipeline and fulfills queued promises

        Returns:
            Futures {list} - list of promises will filled values
        """
        results = self._pipe.execute()
        self._fulfill_futures(results)
        return self._futures

    def _fulfill_futures(self, results):
        for index, value in enumerate(results):
            self._futures[index].fulfill(value)

    def __getattr__(self, name):
        inner_attribute = getattr(self._pipe, name)
        if inner_attribute:
            return self._wrapped_pipeline_call(inner_attribute)

        raise AttributeError(self._missing_attribute_message(name))

    def _wrapped_pipeline_call(self, attribute):
        def callback(*args, **kwargs):
            import promise
            attribute(*args, **kwargs)
            future = promise.Promise()
            self._futures.append(future)
            return future
        return callback

    def _missing_attribute_message(self, name):
        return "'{}' object has no attribute '{}'".format(self._klass.__name__, name)
