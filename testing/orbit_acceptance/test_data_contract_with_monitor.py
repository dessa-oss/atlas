"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
from foundations_spec import *
from foundations_orbit import DataContract

class TestDataContractWithMonitor(Spec):

    @let
    def reference_dataframe(self):
        import pandas
        return pandas.DataFrame(self._create_rows(1000))

    @let
    def contract_name(self):
        return self.faker.name()

    @let
    def reference_dataframe_nans(self):
        import pandas, numpy
        dataframe = pandas.DataFrame(self._create_rows(1000))
        return dataframe.mask(numpy.random.random(dataframe.shape) < .1)

    def _create_rows(self, num=1):
        import numpy
        random_words = [self.faker.word() for _ in range(5)]
        output = [
            {
                "cat_string":numpy.random.choice(random_words),
                "string":self.faker.word(),
                "date_time":self.faker.date_time(),
                "booleans":self.faker.pybool(),
                "cat_int":numpy.random.choice([1,2,3,4,5]),
                "integers":self.faker.pyint(),
                "floats":self.faker.pyint()/17
            } 
            for x in range(num)]
                
        return output

    @skip('not complete')
    def test_data_contract_with_monitor(self):
        contract = DataContract(self.contract_name, self.reference_dataframe)
        contract.save('/tmp/data_contracts')

        contract = DataContract.load('/tmp/data_contracts', self.contract_name)

        validation_results = contract.validate(self.reference_dataframe)

        self._assert_validation_results_has_correct_structure(validation_results)

    def _assert_validation_results_has_correct_structure(self, validation_results):
         for key in ['dist_check_results', 'metadata', 'min_max_test_results', 'row_count', 'schema_check_results', 'special_values_check_results']:
             self.assertIn(key, validation_results.keys())