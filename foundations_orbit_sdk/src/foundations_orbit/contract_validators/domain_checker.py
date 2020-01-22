"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 01 2020
"""


class DomainChecker:
    def validate(self):
        return {
            'summary': {
                'healthy': 0,
                'critical': 0,
                'warning': 0
            },
            'details_by_attribute': []
        }
