"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class DataContract(object):
    
    def __init__(self, contract_name):
        import numpy
        from foundations_orbit.data_contract_options import DataContractOptions

        self.options = DataContractOptions(
            max_bins=50,
            check_schema=True,
            check_row_count=False,
            special_values=[numpy.nan]
        )