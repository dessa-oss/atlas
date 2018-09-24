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

    def evaluate(self):
        """Calls the action callback and returns the result. 
        Also ensures that parent responses are evaluated.

        Returns:
            object -- The return value of the evaluated callback
        """

        if self._parent is not None:
            self._parent.evaluate()
        return self._action_callback()

    def as_json(self):
        from foundations_rest_api.v1.models.property_model import PropertyModel

        result = self.evaluate()

        if isinstance(result, list):
            return [self._value_as_json(value) for value in result]

        if self._is_property_model(result):
            result = result.attributes

        if isinstance(result, dict):
            return self._dictionary_attributes(result)

        return result

    def _dictionary_attributes(self, value):
        attributes = {}
        for key, value in value.items():
            attributes[key] = self._value_as_json(value)
        return attributes

    def _value_as_json(self, value):
        if self._is_response(value):
            return value.as_json()

        if self._is_property_model(value):
            return value.attributes

        return value

    def _is_response(self, value):
        return isinstance(value, Response)

    def _is_property_model(self, value):
        from foundations_rest_api.v1.models.property_model import PropertyModel
        return isinstance(value, PropertyModel)
