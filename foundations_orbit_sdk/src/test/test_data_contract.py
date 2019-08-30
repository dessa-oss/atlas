"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit.data_contract import DataContract

class TestDataContract(Spec):

    @let
    def contract_name(self):
        return self.faker.word()

    @let_now
    def datetime_today(self):
        return self.faker.date_time()

    @set_up
    def set_up(self):
        datetime = self.patch('datetime.datetime')
        datetime.today.return_value = self.datetime_today

    def test_can_import_data_contract_from_foundations_orbit_top_level(self):
        import foundations_orbit
        self.assertEqual(DataContract, foundations_orbit.DataContract)

    def test_data_contract_has_contract_name(self):
        contract = DataContract(self.contract_name)
        self.assertEqual(self.contract_name, contract.contract_name)

    def test_data_contract_has_datetime_as_datetime_today(self):
        contract = DataContract(self.contract_name)
        self.assertEqual(self.datetime_today, contract.datetime)