"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Response(object):
    """Common response object used across the project for running
    post processing against data to be sent to front end applications.

    Arguments:
        resource_name {str} -- Name of the resource type being acted upon
        action_callback {function} -- Method to call when evaluating

    Keyword Arguments:
        parent {Response} -- Parent response to evaluate (default: {None})
    """
    
    @staticmethod
    def constant(value, status=200):
        return Response('Constant', Response._constant_lazy_result(value), status=status)

    @staticmethod
    def _constant_lazy_result(value):
        from foundations_rest_api.lazy_result import LazyResult
        return LazyResult(lambda: value)

    def __init__(self, resource_name, lazy_result, fallback=None, status=200, parent=None):
        self._lazy_result = lazy_result
        self._parent = parent
        self._fallback = fallback
        self._status = status
        self._resource_name = resource_name

    def evaluate(self):
        """Calls the action callback and returns the result.
        Also ensures that parent responses are evaluated.

        Returns:
            object -- The return value of the evaluated callback
        """

        if self._parent is not None:
            self._parent.evaluate()
        return self._lazy_result.evaluate()

    def as_json(self):
        json = self._as_json()
        if json is None:
            return self._get_fallback().as_json()
        return json

    def _as_json(self):
        result = self.evaluate()
        if result is None:
            return None
        return self._value_as_json(result)

    def status(self):
        """Returns the set status code or the fallback if no data
        is available

        Returns:
            int -- Whatever the status code was set to for this or the fallback
        """

        result = self.evaluate()
        if result is None:
            return self._get_fallback().status()
        return self._status
    
    def resource_name(self):
        return self._resource_name

    def _get_fallback(self):
        if self._fallback is None:
            raise ValueError('No response data and no fallback provided!')
        return self._fallback

    def _dictionary_attributes(self, value):
        attributes = {}
        for key, value in value.items():
            attributes[key] = self._value_as_json(value)
        return attributes

    def _value_as_json(self, value):
        import math

        if isinstance(value, list):
            return [self._value_as_json(value) for value in value]

        if self._is_property_model(value):
            return self._dictionary_attributes(value.attributes)

        if isinstance(value, dict):
            return self._dictionary_attributes(value)

        if isinstance(value, float) and math.isnan(value):
            return None

        return value

    def _is_lazy_result(self, value):
        from foundations_rest_api.lazy_result import LazyResult
        return isinstance(value, LazyResult)

    def _is_property_model(self, value):
        from foundations_rest_api.v1.models.property_model import PropertyModel
        return isinstance(value, PropertyModel)
    
