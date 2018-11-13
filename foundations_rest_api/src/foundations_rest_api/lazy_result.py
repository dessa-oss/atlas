"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

class LazyResult(object):

    def __init__(self, callback):
        self._callback = callback

    def only(self, only_fields):

        def filter_properties(value, only_fields):
            is_dict = isinstance(value, dict)
            if only_fields:
                attributes = {}
                for key in only_fields:
                    if is_dict:
                        attributes[key] = value[key]
                    else:
                        attributes[key] = getattr(value, key, None)
                return attributes
            return value

        def lazy_only():
            from foundations_rest_api.v1.models.property_model import PropertyModel
            result = self.evaluate()
            if isinstance(result, list):
                result = [filter_properties(item, only_fields) for item in result]
            elif isinstance(result, PropertyModel):
                result = filter_properties(result.attributes, only_fields)
            elif isinstance(result, LazyResult):
                result = filter_properties(result.evaluate(), only_fields)
            else:
                result = filter_properties(result, only_fields)
            return result

        return LazyResult(lazy_only)

    def filter(self, result_filters, params, fields=[]):

        def filter_field(result):
            from .result_filters import result_filters
            for field in fields:
                data = result[field]
                for result_filter in result_filters:
                    data = result_filter(data, params)
                result[field] = data
            return result

        def filter_result():
            result = self.evaluate()
            if isinstance(result, list):
                result = [filter_field(item) for item in result]
            else:
                result = filter_field(result)
            return result

        return LazyResult(filter_result)

    def evaluate(self):
        result = self._callback()
        if isinstance(result, list):
            return [(item.evaluate() if self._is_lazy_result(item) else item) for item in result ]

        if self._is_lazy_result(result):
            return result.evaluate()

        if isinstance(result, dict):
            return self._evaluate_dict(result)

        return result

    def _is_lazy_result(self, value):
        return isinstance(value, LazyResult)

    def _is_property_model(self, value):
        from foundations_rest_api.v1.models.property_model import PropertyModel
        return isinstance(value, PropertyModel)

    def _evaluate_dict(self, value):
        attributes = {}
        for key, value in value.items():
            attributes[key] = value.evaluate() if self._is_lazy_result(value) else value
        return attributes
