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

        self._contract_name = contract_name

        default_distribution = {
            'distance_metric': 'l_infinity',
            'default_threshold': 0.1,
            'cols_to_include': None,
            'cols_to_ignore': None,
            'custom_thresholds': {}
        }

        self.options = DataContractOptions(
            max_bins=50,
            check_schema=True,
            check_row_count=False,
            special_values=[numpy.nan],
            check_distribution=True,
            distribution=default_distribution
        )

    def save(self, model_package_directory):
        with open(self._data_contract_file_path(model_package_directory), 'wb') as contract_file:
            contract_file.write(self._serialized_contract())

    @staticmethod
    def load(model_package_directory, contract_name):
        import pickle

        with open(f'{model_package_directory}/{contract_name}.pkl', 'rb') as contract_file:
            return pickle.loads(contract_file.read())

    def __eq__(self, other):
        return self._contract_name == other._contract_name

    def _data_contract_file_path(self, model_package_directory):
        return f'{model_package_directory}/{self._contract_name}.pkl'

    def _serialized_contract(self):
        import pickle

        contract = DataContract(self._contract_name)
        contract.options = self.options

        return pickle.dumps(contract)