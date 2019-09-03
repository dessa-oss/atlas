"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit import DataContract

class TestDataValidation(Spec):

    @let
    def reference_dataframe(self):
        import numpy
        import pandas

        return pandas.DataFrame(numpy.random.uniform(-1, 1, size=(100, 2)), columns=['feat_1', 'feat_2'])

    @let
    def reference_dataframe_different_schema(self):
        import numpy
        import pandas

        return pandas.DataFrame(numpy.random.uniform(-1, 1, size=(100, 4)), columns=[f'feat_{i}' for i in range(4)])

    @let
    def dataframe_with_nans(self):
        import numpy

        dataframe_with_nans = self.reference_dataframe.copy()
        dataframe_with_nans.iloc[:50, 0] = numpy.nan
        return dataframe_with_nans

    @let
    def dataframe_with_shifted_distribution(self):
        import numpy

        dataframe_with_shifted_distribution = self.reference_dataframe.copy()
        dataframe_with_shifted_distribution['feat_2'] = numpy.random.uniform(0, 2, size=(100, 1))
        return dataframe_with_shifted_distribution

    @let
    def contract_name(self):
        return 'test_data_contract'

    @let
    def model_package_dirpath(self):
        return 'models/test_model'

    @let
    def contract_filepath(self):
        return f'{self.model_package_dirpath}/{self.contract_name}.pkl'

    @set_up_class
    def set_up_class(klass):
        import numpy
        numpy.random.seed(42)

    @set_up
    def set_up(self):
        import os
        import os.path as path
        import shutil

        if path.isdir(self.model_package_dirpath):
            shutil.rmtree(self.model_package_dirpath)
        os.makedirs(self.model_package_dirpath, exist_ok=True)

    def test_can_load_saved_data_contract(self):
        import os.path as path

        data_contract = DataContract(self.contract_name, df=self.reference_dataframe)
        data_contract.options.schema_check = False
        data_contract.save(self.model_package_dirpath)

        self.assertTrue(path.isfile(self.contract_filepath))

        loaded_data_contract = DataContract.load(self.model_package_dirpath, self.contract_name)
        self.assertEqual(data_contract, loaded_data_contract)

    def test_validate_dataframe_against_own_schema_passes_all_tests(self):
        import datetime
        import numpy

        expected_distribution_report = {
            'feat_1': {
                'binned_l_infinity': 0.0,
                'binned_passed': True,
                'special_values': {
                    numpy.nan: {
                        'current_percentage': 0.0,
                        'passed': True,
                        'percentage_diff': 0.0,
                        'ref_percentage': 0.0
                    }
                }
            },
            'feat_2': {
                'binned_l_infinity': 0.0,
                'binned_passed': True,
                'special_values': {
                    numpy.nan: {
                        'current_percentage': 0.0,
                        'passed': True,
                        'percentage_diff': 0.0,
                        'ref_percentage': 0.0
                    }
                }
            }
        }

        data_contract = DataContract(self.contract_name, df=self.reference_dataframe)
        validation_report = data_contract.validate(self.reference_dataframe, datetime.datetime.today())

        schema_check_passed = validation_report['schema_check_passed']
        distribution_report = validation_report['dist_check_results']

        self.assertTrue(schema_check_passed)
        self.assertEqual(expected_distribution_report, distribution_report)

    @skip
    def test_get_schema_validation_failure_when_column_missing(self):
        data_contract = DataContract(self.contract_name, df=self.reference_dataframe_different_schema)

        dataframe_with_different_column_names = self.reference_dataframe_different_schema.copy().rename({'feat_1': 'feat_x'}, axis=1)
        validation_report = dataframe_with_different_column_names.validate(wrong_reference_dataframe_different_schema, datetime.datetime.today())

        schema_check_passed = validation_report['schema_check_passed']

        self.assertFalse(schema_check_passed)

    @skip
    def test_get_schema_validation_error_when_new_column_added(self):
        data_contract = DataContract(self.contract_name, df=self.reference_dataframe_different_schema)

        dataframe_different_column_sets = self.reference_dataframe_different_schema.copy()
        dataframe_different_column_sets['feat_x'] = 1

        validation_report = data_contract.validate(dataframe_different_column_sets, datetime.datetime.today())

        schema_check_passed = validation_report['schema_check_passed']
        schema_failure_reason = validation_report['schema_check_failure_information']['error_message']

        self.assertFalse(schema_check_passed)
        self.assertEqual('column sets not equal', schema_failure_reason)

    @skip
    def test_get_schema_validation_error_when_columns_in_wrong_order(self):
        data_contract = DataContract(self.contract_name, df=self.reference_dataframe_different_schema)

        dataframe_columns_wrong_order = self.reference_dataframe_different_schema.copy()[['feat_2', 'feat_1', 'feat_3', 'feat_0']]
        validation_report = data_contract.validate(dataframe_columns_wrong_order, datetime.datetime.today())

        schema_check_passed = validation_report['schema_check_passed']
        schema_failure_reason = validation_report['schema_check_failure_information']['error_message']

        self.assertFalse(schema_check_passed)
        self.assertEqual('column not in order', schema_failure_reason)

    @skip
    def test_get_schema_validation_error_when_there_is_a_data_type_mismatch_(self):
        data_contract = DataContract(self.contract_name, df=self.reference_dataframe_different_schema)

        dataframe_different_data_type = self.reference_dataframe_different_schema.copy()
        dataframe_different_data_type['feat_2'] = dataframe_different_data_type['feat_2'].astype(int)

        validation_report = data_contract.validate(dataframe_different_data_type, datetime.datetime.today())

        schema_check_passed = validation_report['schema_check_passed']
        schema_failure_reason = validation_report['schema_check_failure_information']['error_message']

        self.assertFalse(schema_check_passed)
        self.assertEqual('column data type mismatches', schema_failure_reason)

    @skip
    def test_dataframe_with_nans_passes_schema_validation_and_gives_different_distribution_report(self):
        import numpy

        expected_distribution_report = {
            'feat_1': {
                'binned_l_infinity': 0.02,
                'binned_passed': True,
                'special_values': {
                    numpy.nan: {
                        'current_percentage': 0.5,
                        'passed': False,
                        'percentage_diff': 0.5,
                        'ref_percentage': 0.0
                    }
                }
            },
            'feat_2': {
                'binned_l_infinity': 0.0,
                'binned_passed': True,
                'special_values': {
                    numpy.nan: {
                        'current_percentage': 0.0,
                        'passed': True,
                        'percentage_diff': 0.0,
                        'ref_percentage': 0.0
                    }
                }
            }
        }

        data_contract = DataContract(self.contract_name, df=self.reference_dataframe)
        validation_report = data_contract.validate(self.dataframe_with_nans)

        schema_check_passed = validation_report['schema_check_passed']
        distribution_report = validation_report['dist_check_results']

        self.assertTrue(schema_check_passed)
        self.assertEqual(expected_distribution_report, distribution_report)

    @skip
    def test_data_with_shifted_distribution_passes_schema_check_with_different_distribution_report(self):
        import numpy

        expected_distribution_report = {
            'feat_1': {
                'binned_l_infinity': 0.0,
                'binned_passed': True,
                'special_values': {
                    numpy.nan: {
                        'current_percentage': 0.0,
                        'passed': True,
                        'percentage_diff': 0.0,
                        'ref_percentage': 0.0
                    }
                }
            },
            'feat_2': {
                'binned_l_infinity': 0.58,
                'binned_passed': False,
                'special_values': {
                    numpy.nan: {
                        'current_percentage': 0.0,
                        'passed': True,
                        'percentage_diff': 0.0,
                        'ref_percentage': 0.0
                    }
                }
            }
        }

        data_contract = DataContract(self.contract_name, df=self.reference_dataframe)
        validation_report = data_contract.validate(self.dataframe_with_shifted_distribution)

        schema_check_passed = validation_report['schema_check_passed']
        distribution_report = validation_report['dist_check_results']

        self.assertTrue(schema_check_passed)
        self.assertEqual(expected_distribution_report, distribution_report)