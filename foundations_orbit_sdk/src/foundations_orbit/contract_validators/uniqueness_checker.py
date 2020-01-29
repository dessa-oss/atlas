"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Calvin Choi <c.choi@dessa.com>, 01 2020
"""

class UniquenessChecker:
    
    def validate(self, dataframe_to_validate):
        
        return {
            'summary': {},
            'details_by_attribute': []
        }