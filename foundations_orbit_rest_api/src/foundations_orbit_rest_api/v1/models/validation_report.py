"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ValidationReport(object):
    
    @staticmethod
    def get(**kwargs):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        return LazyResult(ValidationReport._get_internal)

    @staticmethod
    def _get_internal():
        return None