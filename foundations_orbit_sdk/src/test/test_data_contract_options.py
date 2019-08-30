"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit.data_contract_options import DataContractOptions

class TestDataContractOptions(Spec):
    
    @let
    def max_bins(self):
        return self.faker.random.randint(1, 100)

    def test_data_contract_options_has_max_bins(self):
        options = DataContractOptions(max_bins=self.max_bins)
        self.assertEqual(self.max_bins, options.max_bins)