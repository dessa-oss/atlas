"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

class LazyResult(object):

    def __init__(self, callback):
        self._callback = callback
        self._result = None

    def only(self, only_fields):

        def set_attributes_fields(attributes, key, container):
            if isinstance(container, dict):
                attributes[key] = container[key]
            else:
                attributes[key] = getattr(container, key, None)

        def filter_properties(value, only_fields):
            if only_fields:
                attributes = {}
                for key in only_fields:
                    set_attributes_fields(attributes, key, value)
                return attributes
            return value

        def lazy_only():
            from foundations_rest_api.v1.models.property_model import PropertyModel

            result = self.evaluate(only_fields)

            if isinstance(result, list):
                return [filter_properties(item, only_fields) for item in result]

            if isinstance(result, PropertyModel):
                return filter_properties(result.attributes, only_fields)

            if isinstance(result, LazyResult):
                return filter_properties(result.evaluate(), only_fields)

            if isinstance(result, dict):
                return filter_properties(result, only_fields)

            return result

        return LazyResult(lazy_only)

    def apply_filters(self, params, fields=[]):

        def filter_by_param(field, result, filter_detection_key):
            from foundations_rest_api.filters import get_api_filters
            api_filter = get_api_filters(filter_detection_key)
            # TODO: Avoid the same filter to be run more than once on the same field
            if api_filter:
                data = result[field]
                data = api_filter(data, params)
                result[field] = data

        def filter_field(field, result):
            for param_key in params.keys():
                filter_detection_key = param_key.rsplit('_', 1)[-1]
                filter_by_param(field, result, filter_detection_key)

        def filter_all_fields(result):
            for field in fields:
                filter_field(field, result)
            return result

        def filter_result():
            result = self.evaluate()
            if isinstance(result, list):
                result = [filter_all_fields(item) for item in result]
            else:
                result = filter_all_fields(result)
            return result

        return LazyResult(filter_result)

    def evaluate(self, only_fields=None):
        from foundations_rest_api.v1.models.property_model import PropertyModel

        if self._result is not None:
            return self._result

        result = self._callback()

        if isinstance(result, list):
            self._result = [(item.evaluate(only_fields) if self._is_lazy_result(item) else item) for item in result ]
            return self._result

        if self._is_lazy_result(result):
            self._result = result.evaluate(only_fields)
            return self._result

        if isinstance(result, PropertyModel):
            self._result = self._evaluate_property_model(result, only_fields)
            return self._result

        if isinstance(result, dict):
            self._result = self._evaluate_dict(result)
            return self._result

        self._result = result
        return self._result

    def map(self, callback):
        def _inner():
            result = self.evaluate()
            return callback(result)
        return LazyResult(_inner)

    def _is_lazy_result(self, value):
        return isinstance(value, LazyResult)

    def _evaluate_dict(self, value):
        attributes = {}
        for key, value in value.items():
            attributes[key] = value.evaluate() if self._is_lazy_result(value) else value
        return attributes

    def _evaluate_property_model(self, value, only_fields):
        for property_name, property_value in value.attributes.items():
            if self._is_lazy_result(property_value):
                if only_fields is None or property_name in only_fields:
                  setattr(value, property_name, property_value.evaluate())
        return value
