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

    def __init__(self, resource_name, action_callback, parent=None):
        self._action_callback = action_callback
        self._parent = parent
        self._only = None
        self._params = None

    def evaluate(self):
        """Calls the action callback and returns the result. 
        Also ensures that parent responses are evaluated.

        Returns:
            object -- The return value of the evaluated callback
        """

        if self._parent is not None:
            self._parent.evaluate()
        return self._action_callback()

    def only(self, only):
        self._only = only
        return self

    def filter(self, params):
        self._params = params
        return self

    def as_json(self):
        from foundations_rest_api.v1.models.property_model import PropertyModel

        result = self.evaluate()

        if self._params:
            resullt = self._filter_result(result)

        if isinstance(result, list):
            return [self._value_as_json(value, self._only) for value in result]

        if self._is_property_model(result):
            result = self._filtered_properties(result)

        if isinstance(result, dict):
            return self._dictionary_attributes(result)

        return result

    def _filtered_properties(self, value):
        value = value.attributes
        if self._only:
            attributes = {}
            for key in self._only:
                attributes[key] = value[key]
            return  attributes

        return value

    def _dictionary_attributes(self, value):
        attributes = {}
        for key, value in value.items():
            attributes[key] = self._value_as_json(value)
        return attributes

    def _value_as_json(self, value, only=None):
        if self._is_response(value):
            return value.only(only).as_json()

        if self._is_property_model(value):
            return self._filtered_properties(value)

        return value

    def _is_response(self, value):
        return isinstance(value, Response)

    def _is_property_model(self, value):
        from foundations_rest_api.v1.models.property_model import PropertyModel
        return isinstance(value, PropertyModel)

    def _filter_result(self, result):
        from .result_filters import result_filters
        for result_filter in result_filters:
            result = result_filter(result, self._params)
        return result
