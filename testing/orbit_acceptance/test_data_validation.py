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
    def reference_dataframe_different_schema_and_type(self):
        import numpy
        import pandas

        return pandas.DataFrame(numpy.random.uniform(-1, 1, size=(100, 4)), columns=[f'feat_{i}' for i in range(4)], dtype=float)

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
    def monitor_package_dirpath(self):
        return 'models/test_model'

    @let
    def contract_filepath(self):
        return f'{self.monitor_package_dirpath}/{self.contract_name}.pkl'

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def monitor_name(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        import os
        import os.path as path
        import shutil

        import numpy
        numpy.random.seed(42)

        if path.isdir(self.monitor_package_dirpath):
            shutil.rmtree(self.monitor_package_dirpath)
        os.makedirs(self.monitor_package_dirpath, exist_ok=True)

        self._old_project_name = os.environ.get('PROJECT_NAME')
        self._old_monitor_name = os.environ.get('MONITOR_NAME')

        os.environ['PROJECT_NAME'] = self.project_name
        os.environ['MONITOR_NAME'] = self.monitor_name

    @tear_down
    def tear_down(self):
        import os

        if self._old_project_name is not None:
            os.environ['PROJECT_NAME'] = self._old_project_name
        elif 'PROJECT_NAME' in os.environ:
            os.environ.pop('PROJECT_NAME')

        if self._old_monitor_name is not None:
            os.environ['MONITOR_NAME'] = self._old_monitor_name
        elif 'MONITOR_NAME' in os.environ:
            os.environ.pop('MONITOR_NAME')

    def test_can_load_saved_data_contract(self):
        import os.path as path

        data_contract = DataContract(self.contract_name, df=self.reference_dataframe)
        data_contract.save(self.monitor_package_dirpath)

        self.assertTrue(path.isfile(self.contract_filepath))

        loaded_data_contract = DataContract.load(self.monitor_package_dirpath, self.contract_name)
        self.assertEqual(data_contract, loaded_data_contract)

    def test_validate_dataframe_against_own_schema_passes_all_tests(self):
        import datetime
        import numpy

        expected_distribution_report = {
            'feat_1': {
                'binned_l_infinity': 0.0,
                'binned_passed': True
            },
            'feat_2': {
                'binned_l_infinity': 0.0,
                'binned_passed': True
            }
        }
        expected_special_values_report = {
            'feat_1':{
                numpy.nan: {
                    'current_percentage': 0.0,
                    'passed': True,
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.0
                }
            },
            'feat_2': {
                numpy.nan: {
                    'current_percentage': 0.0,
                    'passed': True,
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.0
                }
            }
        }

        data_contract = DataContract(self.contract_name, df=self.reference_dataframe)
        data_contract.special_value_test.configure(attributes=['feat_1', 'feat_2'], thresholds={numpy.nan: 0.1})
        validation_report = data_contract.validate(self.reference_dataframe, datetime.datetime.today())

        schema_check_passed = validation_report['schema_check_results']['passed']
        distribution_report = validation_report['dist_check_results']
        special_values_report = validation_report['special_values_check_results']

        self.assertTrue(schema_check_passed)
        self.assertEqual(expected_distribution_report, distribution_report)
        self.assertEqual(expected_special_values_report, special_values_report)

    def test_get_schema_validation_failure_when_column_missing(self):
        import datetime

        data_contract = DataContract(self.contract_name, df=self.reference_dataframe_different_schema)

        wrong_reference_dataframe_different_schema = self.reference_dataframe_different_schema.copy().rename({'feat_1': 'feat_x'}, axis=1)
        validation_report = data_contract.validate(wrong_reference_dataframe_different_schema, datetime.datetime.today())

        schema_check_passed = validation_report['schema_check_results']['passed']
        schema_failure_reason = validation_report['schema_check_results']['error_message']
        missing_in_ref = validation_report['schema_check_results']['missing_in_ref']
        missing_in_current = validation_report['schema_check_results']['missing_in_current']

        self.assertFalse(schema_check_passed)
        self.assertEqual('column sets not equal', schema_failure_reason)
        self.assertEqual(['feat_x'], missing_in_ref)
        self.assertEqual(['feat_1'], missing_in_current)

    def test_get_schema_validation_error_when_new_column_added(self):
        import datetime

        data_contract = DataContract(self.contract_name, df=self.reference_dataframe_different_schema)

        dataframe_different_column_sets = self.reference_dataframe_different_schema.copy()
        dataframe_different_column_sets['feat_x'] = 1

        validation_report = data_contract.validate(dataframe_different_column_sets, datetime.datetime.today())

        schema_check_passed = validation_report['schema_check_results']['passed']
        schema_failure_reason = validation_report['schema_check_results']['error_message']
        missing_in_ref = validation_report['schema_check_results']['missing_in_ref']
        missing_in_current = validation_report['schema_check_results']['missing_in_current']

        self.assertFalse(schema_check_passed)
        self.assertEqual('column sets not equal', schema_failure_reason)
        self.assertEqual(['feat_x'], missing_in_ref)
        self.assertEqual([], missing_in_current)

    def test_get_schema_validation_error_when_columns_in_wrong_order(self):
        import datetime

        data_contract = DataContract(self.contract_name, df=self.reference_dataframe_different_schema)

        dataframe_columns_wrong_order = self.reference_dataframe_different_schema.copy()[['feat_0', 'feat_3', 'feat_2', 'feat_1']]
        validation_report = data_contract.validate(dataframe_columns_wrong_order, datetime.datetime.today())

        schema_check_passed = validation_report['schema_check_results']['passed']
        schema_failure_reason = validation_report['schema_check_results']['error_message']
        columns_not_in_order = validation_report['schema_check_results']['columns_out_of_order']

        self.assertFalse(schema_check_passed)
        self.assertEqual('columns not in order', schema_failure_reason)
        self.assertEqual(['feat_3', 'feat_1'], columns_not_in_order)

    def test_get_schema_validation_error_when_there_is_a_data_type_mismatch_(self):
        import datetime

        data_contract = DataContract(self.contract_name, df=self.reference_dataframe_different_schema_and_type)

        dataframe_different_data_type = self.reference_dataframe_different_schema_and_type.copy()
        dataframe_different_data_type['feat_2'] = dataframe_different_data_type['feat_2'].astype(int)

        validation_report = data_contract.validate(dataframe_different_data_type, datetime.datetime.today())

        schema_check_passed = validation_report['schema_check_results']['passed']
        schema_failure_reason = validation_report['schema_check_results']['error_message']
        datatype_mismatch_information = validation_report['schema_check_results']['cols']

        expected_mismatch_information = {
            'feat_2': {
                'ref_type': 'float64',
                'current_type': 'int64'
            }
        }

        self.assertFalse(schema_check_passed)
        self.assertEqual('column datatype mismatches', schema_failure_reason)
        self.assertEqual(expected_mismatch_information, datatype_mismatch_information)

    def test_dataframe_with_nans_passes_schema_validation_and_gives_different_distribution_report(self):
        import numpy

        expected_distribution_report = {
            'feat_1': {
                'binned_l_infinity': 0.02,
                'binned_passed': True
            },
            'feat_2': {
                'binned_l_infinity': 0.0,
                'binned_passed': True
            }
        }
        expected_special_values_report = {
            'feat_1':{
                numpy.nan: {
                    'current_percentage': 0.5,
                    'passed': False,
                    'percentage_diff': 0.5,
                    'ref_percentage': 0.0
                }
            },
            'feat_2': {
                numpy.nan: {
                    'current_percentage': 0.0,
                    'passed': True,
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.0
                }
            }
        }

        data_contract = DataContract(self.contract_name, df=self.reference_dataframe)
        data_contract.special_value_test.configure(attributes=['feat_1', 'feat_2'], thresholds={numpy.nan: 0.1})
        validation_report = data_contract.validate(self.dataframe_with_nans)

        schema_check_passed = validation_report['schema_check_results']['passed']
        distribution_report = validation_report['dist_check_results']
        special_values_report = validation_report['special_values_check_results']

        self.assertTrue(schema_check_passed)
        self.assertEqual(expected_distribution_report, distribution_report)
        self.assertEqual(expected_special_values_report, special_values_report)

    def test_data_with_shifted_distribution_passes_schema_check_with_different_distribution_report(self):
        import numpy

        expected_distribution_report = {
            'feat_1': {
                'binned_l_infinity': 0.0,
                'binned_passed': True
            },
            'feat_2': {
                'binned_l_infinity': 0.58,
                'binned_passed': False
            }
        }
        expected_special_values_report = {
            'feat_1':{
                numpy.nan: {
                    'current_percentage': 0.0,
                    'passed': True,
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.0
                }
            },
            'feat_2': {
                numpy.nan: {
                    'current_percentage': 0.0,
                    'passed': True,
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.0
                }
            }
        }

        data_contract = DataContract(self.contract_name, df=self.reference_dataframe)
        data_contract.special_value_test.configure(attributes=['feat_1', 'feat_2'], thresholds={numpy.nan: 0.1})
        validation_report = data_contract.validate(self.dataframe_with_shifted_distribution)

        schema_check_passed = validation_report['schema_check_results']['passed']
        distribution_report = validation_report['dist_check_results']
        special_values_report = validation_report['special_values_check_results']

        self.assertTrue(schema_check_passed)
        self.assertEqual(expected_distribution_report, distribution_report)
        self.assertEqual(expected_special_values_report, special_values_report)

    def test_ensure_can_retrieve_validation_results_from_rest_api_via_the_dv_model(self):
        import numpy
        import subprocess
        from foundations_orbit_rest_api.v1.models.validation_report import ValidationReport
        from foundations_orbit_rest_api.v1.models.validation_report_listing import ValidationReportListing
        subprocess.run(['python', 'create_data_contract.py'], cwd='orbit_acceptance/fixtures/data_validation')

        inference_period='2019-09-01'
        contract_name = 'dv_contract'
        data_contract = DataContract.load('/tmp', contract_name)
        data_contract.validate(self.dataframe_with_shifted_distribution, inference_period=inference_period)
        
        report_listing = ValidationReportListing(inference_period=inference_period, monitor_package=self.monitor_name, data_contract=contract_name)
        api_validation_report = ValidationReport.get(project_name=self.project_name, listing_object=report_listing).evaluate()

        expected_validation_report = {
            'attribute_names': ['feat_1', 'feat_2'],
            'date': inference_period,
            'monitor_package': self.monitor_name,
            'data_contract': contract_name,
            'row_count': {
                'expected_row_count': 100,
                'actual_row_count': len(self.dataframe_with_shifted_distribution),
                'row_count_diff': 0.0
            },
            'schema': {
                'summary': {
                    'healthy': 2, 'critical': 0, 'warning': 0
                },
                'details_by_attribute': [
                    {
                        'attribute_name': 'feat_1',
                        'data_type': 'float64',
                        'issue_type': None,
                        'validation_outcome': 'healthy'
                    },
                    {
                        'attribute_name': 'feat_2',
                        'data_type': 'float64',
                        'issue_type': None,
                        'validation_outcome': 'healthy'
                    }
                ]
            },
            'data_quality': {
                'details_by_attribute': [
                    {
                        'attribute_name': 'feat_1',
                        'value': 'nan',
                        'pct_in_reference_data': 0.0,
                        'pct_in_current_data': 0.0,
                        'difference_in_pct': 0.0,
                        'validation_outcome': 'healthy'
                    },
                    {
                        'attribute_name': 'feat_2',
                        'value': 'nan',
                        'pct_in_reference_data': 0.0,
                        'pct_in_current_data': 0.0,
                        'difference_in_pct': 0.0,
                        'validation_outcome': 'healthy'
                    }
                ],
                'summary': {
                    'critical': 0,
                    'healthy': 2,
                    'warning': 0
                }
            },
            'population_shift': {
                'details_by_attribute': [
                    {
                        'attribute_name': 'feat_1',
                        'L-infinity': 0.0,
                        'validation_outcome': 'healthy'
                    },
                    {
                        'attribute_name': 'feat_2',
                        'L-infinity': 0.58,
                        'validation_outcome': 'critical'
                    }
                ],
                'summary': {
                    'critical': 1, 'healthy': 1, 'warning': 0
                }
            },
            'max': {
                'details_by_attribute': [],
                'summary': {
                    'critical': 0,
                    'healthy': 0,
                    'warning': 0
                }
            },
            'min': {
                'details_by_attribute': [],
                'summary': {
                    'critical': 0,
                    'healthy': 0,
                    'warning': 0
                }
            }
        }

        del api_validation_report['uuid']

        self.assertIn('user', api_validation_report)
        del api_validation_report['user']
        self.assertIn('job_id', api_validation_report)
        del api_validation_report['job_id']

        expected_validation_report['data_quality']['details_by_attribute'] = sorted(expected_validation_report['data_quality']['details_by_attribute'], key=lambda data: data['attribute_name'])
        api_validation_report['data_quality']['details_by_attribute'] = sorted(api_validation_report['data_quality']['details_by_attribute'], key=lambda data: data['attribute_name'])

        self.assertEqual(expected_validation_report, api_validation_report)

    def test_dataframe_with_nans_for_configuring_and_excluding_method_on_special_values_test(self):
        import numpy

        expected_special_values_report = {
            'feat_1':{
                numpy.nan: {
                    'current_percentage': 0.5,
                    'passed': True,
                    'percentage_diff': 0.5,
                    'ref_percentage': 0.0
                }
            }
        }

        dc = DataContract(self.contract_name, df=self.reference_dataframe)
        dc.special_value_test.exclude(attributes='all')
        dc.special_value_test.configure(attributes=['feat_1'], thresholds={ numpy.nan: 0.6 })
        validation_report = dc.validate(self.dataframe_with_nans)
        special_values_report = validation_report['special_values_check_results']

        self.assertEqual(expected_special_values_report, special_values_report)

    def test_dataframe_with_nans_for_multiple_call_of_configure_method_on_special_values_test(self):
        import numpy

        expected_special_values_report = {
            'feat_1':{
                numpy.nan: {
                    'current_percentage': 0.5,
                    'passed': True,
                    'percentage_diff': 0.5,
                    'ref_percentage': 0.0
                }
            },
            'feat_2': {
                numpy.nan: {
                    'current_percentage': 0.0,
                    'passed': True,
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.0
                }
            }
        }

        dc = DataContract(self.contract_name, df=self.reference_dataframe)
        dc.special_value_test.exclude(attributes='all')
        dc.special_value_test.configure(attributes=['feat_1'], thresholds={ numpy.nan: 0.6 })
        dc.special_value_test.configure(attributes=['feat_2'], thresholds={ numpy.nan: 0.6 })
        validation_report = dc.validate(self.dataframe_with_nans)
        special_values_report = validation_report['special_values_check_results']

        self.assertEqual(expected_special_values_report, special_values_report)

    def test_dataframe_with_nans_and_minus_one_as_special_values_for_different_columns(self):
        self.maxDiff = None
        import numpy

        expected_special_values_report = {
            'feat_0':{
                numpy.nan: {
                    'current_percentage': 0.0,
                    'passed': True,
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.0
                }
            },
            'feat_1': {
                numpy.nan: {
                    'current_percentage': 0.5,
                    'passed': True,
                    'percentage_diff': 0.5,
                    'ref_percentage': 0.0
                },
                -1: {
                    'current_percentage': 0.0,
                    'passed': True,
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.0
                }
            },
            'feat_2': {
                numpy.nan: {
                    'current_percentage': 0.0,
                    'passed': True,
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.0
                },
                -1: {
                    'current_percentage': 0.5,
                    'passed': False,
                    'percentage_diff': 0.5,
                    'ref_percentage': 0.0
                }
            }
        }

        dc = DataContract(self.contract_name, df=self.reference_dataframe_different_schema)
        dataframe_to_validate = self.reference_dataframe_different_schema.copy()

        dataframe_to_validate.iloc[:50, 1] = numpy.nan
        dataframe_to_validate.iloc[:50, 2] = -1

        dc.special_value_test.exclude(attributes='all')
        dc.special_value_test.configure(attributes=['feat_0'], thresholds={numpy.nan: 0.6})

        dc.special_value_test.configure(attributes=['feat_1', 'feat_2'], thresholds={numpy.nan: 0.6, -1: 0.1})
        validation_report = dc.validate(dataframe_to_validate)

        special_values_report = validation_report['special_values_check_results']

        self.assertEqual(expected_special_values_report, special_values_report)