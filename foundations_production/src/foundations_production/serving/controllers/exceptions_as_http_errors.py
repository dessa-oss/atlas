"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

def exceptions_as_http_errors(method):
    from functools import wraps

    @wraps(method)
    def method_decorator(*args, **kwargs):
        from flask import request, abort
        from werkzeug.exceptions import NotFound, BadRequestKeyError
        from foundations_production.exceptions import MissingModelPackageException

        try:
            return method(*args, **kwargs)
        except KeyError as key_error_exception:
            missing_key = key_error_exception.args[0]
            raise BadRequestKeyError(description='Missing field in JSON data: {}'.format(missing_key))
        except MissingModelPackageException as missing_model_packag_exception:
            package_name = missing_model_packag_exception.args[0]
            raise NotFound(description='Model package not found: {}'.format(package_name))

    return method_decorator
