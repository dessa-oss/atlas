"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 06 2018
"""

from foundations_spec import *


class TestDataContractSummary(Spec):

    @let
    def reference_dataframe_with_one_numerical_column(self):
        import pandas
        import numpy

        values = []
        for i in range(1, 12):
            for _ in range(i):
                values.append(i)

        return pandas.DataFrame(data={'feat_1': values}, dtype=numpy.float64)

    @let
    def reference_dataframe_with_one_numerical_column_and_nans(self):
        import pandas
        import numpy

        values = []
        for i in range(1, 12):
            for _ in range(i):
                values.append(i)
        nans = [numpy.nan] * 9
        values.extend(nans)

        return pandas.DataFrame(data={'feat_1': values}, dtype=numpy.float64)

    @let
    def reference_dataframe_with_one_boolean_column(self):
        import pandas
        import numpy

        values = []
        for i in range(1, 12):
            for _ in range(i):
                values.append(i % 2 == 0)

        return pandas.DataFrame(data={'feat_1': values}, dtype=numpy.bool)

    @let
    def reference_dataframe_with_two_numerical_columns(self):
        import pandas
        import numpy

        values_1 = []
        for i in range(1, 12):
            for _ in range(i):
                values_1.append(i)

        values_2 = []
        for i in range(1, 12):
            for _ in range(i):
                values_2.append(12 - i)

        return pandas.DataFrame(data={'feat_1': values_1, 'feat_2': values_2}, dtype=numpy.float64)

    @let
    def dataframe_to_validate_with_one_numerical_column(self):
        import pandas
        import numpy

        values = []
        for i in range(1, 12):
            for _ in range(i):
                values.append(12 - i)

        return pandas.DataFrame(data={'feat_1': values}, dtype=numpy.float64)

    @let
    def dataframe_to_validate_with_one_numerical_column_and_different_attribute_name(self):
        import pandas
        import numpy

        values = []
        for i in range(1, 12):
            for _ in range(i):
                values.append(12 - i)

        return pandas.DataFrame(data={'feat_3': values}, dtype=numpy.float64)

    @let
    def dataframe_to_validate_with_one_numerical_column_and_different_attribute_type(self):
        import pandas
        import numpy

        values = []
        for i in range(1, 12):
            for _ in range(i):
                values.append(12 - i)

        return pandas.DataFrame(data={'feat_1': values}, dtype=numpy.int64)

    @let
    def dataframe_to_validate_with_one_numerical_column_and_nans(self):
        import pandas
        import numpy

        values = []
        for i in range(1, 12):
            for _ in range(i):
                values.append(12 - i)
        nans = [numpy.nan] * 9
        values.extend(nans)

        return pandas.DataFrame(data={'feat_1': values}, dtype=numpy.float64)

    @let
    def dataframe_to_validate_with_two_numerical_columns(self):
        import pandas
        import numpy

        values_1 = []
        for i in range(1, 12):
            for _ in range(i):
                values_1.append(12 - i)

        values_2 = []
        for i in range(1, 12):
            for _ in range(i):
                values_2.append(i)

        return pandas.DataFrame(data={'feat_1': values_1, 'feat_2': values_2}, dtype=numpy.float64)

    def _create_data_contract_summary(self, dataframe):
        from foundations_orbit.data_contract_summary import DataContractSummary
        column_names = list(dataframe.columns)
        column_types = {column_name: str(dataframe.dtypes[column_name]) for column_name in column_names}
        return DataContractSummary(dataframe, column_names, column_types)

    def _create_formatted_report(self, reference_dataframe):
        return {
            'attribute_names': list(reference_dataframe.columns),
            'schema': {
                'summary': {
                    'critical': 0
                }
            },
            'data_quality': {
                'summary': {
                    'critical': 0
                }
            },
            'population_shift': {
                'summary': {
                    'critical': 0
                }
            },
            'min': {
                'summary': {
                    'critical': 0
                }
            },
            'max': {
                'summary': {
                    'critical': 0
                }
            }
        }

    def test_data_contract_summary_has_attribute_data_contract_summary(self):
        data_contract_summary = self._create_data_contract_summary(self.reference_dataframe_with_one_numerical_column)
        self.assertIsNotNone(getattr(data_contract_summary, 'data_contract_summary', None))

    def test_attribute_data_contract_summary_has_key_attribute_summaries(self):
        data_contract_summary = self._create_data_contract_summary(self.reference_dataframe_with_one_numerical_column)
        self.assertIn('attribute_summaries', data_contract_summary.data_contract_summary)

    def test_attribute_summary_has_expected_data_format_before_validate(self):
        data_contract_summary = self._create_data_contract_summary(self.reference_dataframe_with_one_numerical_column)
        attribute_summary = data_contract_summary.data_contract_summary['attribute_summaries']['feat_1']
        self.assertIn('expected_data_summary', attribute_summary)
        self.assertIn('percentage_missing', attribute_summary['expected_data_summary'])
        self.assertIn('minimum', attribute_summary['expected_data_summary'])
        self.assertIn('maximum', attribute_summary['expected_data_summary'])
        self.assertIn('binned_data', attribute_summary)
        self.assertIn('bins', attribute_summary['binned_data'])
        self.assertIn('data', attribute_summary['binned_data'])
        self.assertIn('expected_data', attribute_summary['binned_data']['data'])

    def test_attribute_summary_has_actual_data_format_after_validate(self):
        data_contract_summary = self._create_data_contract_summary(self.reference_dataframe_with_one_numerical_column)
        data_contract_summary.validate(
            self.dataframe_to_validate_with_one_numerical_column,
            self._create_formatted_report(self.reference_dataframe_with_one_numerical_column)
        )
        attribute_summary = data_contract_summary.data_contract_summary['attribute_summaries']['feat_1']
        self.assertIn('actual_data_summary', attribute_summary)
        self.assertIn('percentage_missing', attribute_summary['actual_data_summary'])
        self.assertIn('minimum', attribute_summary['actual_data_summary'])
        self.assertIn('maximum', attribute_summary['actual_data_summary'])
        self.assertIn('binned_data', attribute_summary)
        self.assertIn('bins', attribute_summary['binned_data'])
        self.assertIn('data', attribute_summary['binned_data'])
        self.assertIn('actual_data', attribute_summary['binned_data']['data'])

    def test_data_contract_summary_init_bins_reference_dataframe_with_one_numerical_column(self):
        data_contract_summary = self._create_data_contract_summary(self.reference_dataframe_with_one_numerical_column)
        attribute_summary = data_contract_summary.data_contract_summary['attribute_summaries']['feat_1']

        expected_data = {
            'expected_data_summary': {
                'percentage_missing': 0.0,
                'minimum': 1,
                'maximum': 11
            },
            'binned_data': {
                'bins': ['1.0-2.0', '2.0-3.0', '3.0-4.0', '4.0-5.0', '5.0-6.0', '6.0-7.0', '7.0-8.0', '8.0-9.0',
                         '9.0-10.0', '10.0-11.0'],
                'data': {
                    'expected_data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 21]
                }
            }
        }

        self.assertEqual(expected_data, attribute_summary)

    def test_data_contract_summary_init_bins_reference_dataframe_with_two_numerical_columns(self):
        data_contract_summary = self._create_data_contract_summary(self.reference_dataframe_with_two_numerical_columns)
        attribute_summaries = data_contract_summary.data_contract_summary['attribute_summaries']

        expected_data = {
            'feat_1': {
                'expected_data_summary': {
                    'percentage_missing': 0.0,
                    'minimum': 1,
                    'maximum': 11
                },
                'binned_data': {
                    'bins': ['1.0-2.0', '2.0-3.0', '3.0-4.0', '4.0-5.0', '5.0-6.0', '6.0-7.0', '7.0-8.0', '8.0-9.0',
                             '9.0-10.0', '10.0-11.0'],
                    'data': {
                        'expected_data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 21]
                    }
                }
            },
            'feat_2': {
                'expected_data_summary': {
                    'percentage_missing': 0.0,
                    'minimum': 1,
                    'maximum': 11
                },
                'binned_data': {
                    'bins': ['1.0-2.0', '2.0-3.0', '3.0-4.0', '4.0-5.0', '5.0-6.0', '6.0-7.0', '7.0-8.0', '8.0-9.0',
                             '9.0-10.0', '10.0-11.0'],
                    'data': {
                        'expected_data': [11, 10, 9, 8, 7, 6, 5, 4, 3, 3]
                    }
                }
            }
        }

        self.assertEqual(expected_data, attribute_summaries)

    def test_data_contract_summary_init_bins_reference_dataframe_with_one_numerical_column_with_nans(self):
        data_contract_summary = self._create_data_contract_summary(self.reference_dataframe_with_one_numerical_column_and_nans)
        attribute_summary = data_contract_summary.data_contract_summary['attribute_summaries']['feat_1']

        expected_data = {
            'expected_data_summary': {
                'percentage_missing': 0.12,
                'minimum': 1,
                'maximum': 11
            },
            'binned_data': {
                'bins': ['1.0-2.0', '2.0-3.0', '3.0-4.0', '4.0-5.0', '5.0-6.0', '6.0-7.0', '7.0-8.0', '8.0-9.0',
                         '9.0-10.0', '10.0-11.0'],
                'data': {
                    'expected_data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 21]
                }
            }
        }

        self.assertEqual(expected_data, attribute_summary)

    def test_data_contract_summary_init_does_not_bin_reference_dataframe_with_non_numerical_column(self):
        data_contract_summary = self._create_data_contract_summary(self.reference_dataframe_with_one_boolean_column)
        attribute_summary = data_contract_summary.data_contract_summary['attribute_summaries']['feat_1']
        expected_output = {'expected_data_summary': None, 'binned_data': {'bins': None, 'data': {'expected_data': None}}}
        self.assertEqual(expected_output, attribute_summary)

    def test_data_contract_summary_validation_creates_binned_summary_of_current_dataframe_against_reference_dataframe(self):
        data_contract_summary = self._create_data_contract_summary(self.reference_dataframe_with_two_numerical_columns)
        data_contract_summary.validate(
            self.dataframe_to_validate_with_two_numerical_columns,
            self._create_formatted_report(self.reference_dataframe_with_two_numerical_columns)
        )
        attribute_summaries = data_contract_summary.data_contract_summary['attribute_summaries']

        expected_data = {
            'feat_1': {
                'expected_data_summary': {
                    'percentage_missing': 0.0,
                    'minimum': 1.0,
                    'maximum': 11.0
                },
                'actual_data_summary': {
                    'percentage_missing': 0.0,
                    'minimum': 1.0,
                    'maximum': 11.0
                },
                'binned_data': {
                    'bins': ['1.0-2.0', '2.0-3.0', '3.0-4.0', '4.0-5.0', '5.0-6.0', '6.0-7.0', '7.0-8.0', '8.0-9.0',
                             '9.0-10.0', '10.0-11.0'],
                    'data': {
                        'expected_data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 21],
                        'actual_data': [11, 10, 9, 8, 7, 6, 5, 4, 3, 3]
                    }
                }
            },
            'feat_2': {
                'expected_data_summary': {
                    'percentage_missing': 0.0,
                    'minimum': 1.0,
                    'maximum': 11.0
                },
                'actual_data_summary': {
                    'percentage_missing': 0.0,
                    'minimum': 1.0,
                    'maximum': 11.0
                },
                'binned_data': {
                    'bins': ['1.0-2.0', '2.0-3.0', '3.0-4.0', '4.0-5.0', '5.0-6.0', '6.0-7.0', '7.0-8.0', '8.0-9.0',
                             '9.0-10.0', '10.0-11.0'],
                    'data': {
                        'expected_data': [11, 10, 9, 8, 7, 6, 5, 4, 3, 3],
                        'actual_data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 21]
                    }
                }
            }
        }
        self.assertEqual(expected_data, attribute_summaries)

    def test_data_contract_summary_validation_does_not_create_binned_summary_of_current_dataframe_against_reference_dataframe_when_column_name_mismatch(self):
        data_contract_summary = self._create_data_contract_summary(self.reference_dataframe_with_one_numerical_column)
        data_contract_summary.validate(
            self.dataframe_to_validate_with_one_numerical_column_and_different_attribute_name,
            self._create_formatted_report(self.reference_dataframe_with_one_numerical_column)
        )
        attribute_summaries = data_contract_summary.data_contract_summary['attribute_summaries']

        expected_data = {
            'feat_1': {
                'expected_data_summary': {
                    'percentage_missing': 0.0,
                    'minimum': 1.0,
                    'maximum': 11.0
                },
                'actual_data_summary': None,
                'binned_data': {
                    'bins': ['1.0-2.0', '2.0-3.0', '3.0-4.0', '4.0-5.0', '5.0-6.0', '6.0-7.0', '7.0-8.0', '8.0-9.0',
                             '9.0-10.0', '10.0-11.0'],
                    'data': {
                        'expected_data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 21],
                        'actual_data': None
                    }
                }
            }
        }
        self.assertEqual(expected_data, attribute_summaries)

    def test_data_contract_summary_validation_does_not_create_binned_summary_of_current_dataframe_against_reference_dataframe_when_column_type_mismatch(self):
        data_contract_summary = self._create_data_contract_summary(self.reference_dataframe_with_one_numerical_column)
        data_contract_summary.validate(
            self.dataframe_to_validate_with_one_numerical_column_and_different_attribute_type,
            self._create_formatted_report(self.reference_dataframe_with_one_numerical_column)
        )
        attribute_summaries = data_contract_summary.data_contract_summary['attribute_summaries']

        expected_data = {
            'feat_1': {
                'expected_data_summary': {
                    'percentage_missing': 0.0,
                    'minimum': 1.0,
                    'maximum': 11.0
                },
                'actual_data_summary': None,
                'binned_data': {
                    'bins': ['1.0-2.0', '2.0-3.0', '3.0-4.0', '4.0-5.0', '5.0-6.0', '6.0-7.0', '7.0-8.0', '8.0-9.0',
                             '9.0-10.0', '10.0-11.0'],
                    'data': {
                        'expected_data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 21],
                        'actual_data': None
                    }
                }
            }
        }
        self.assertEqual(expected_data, attribute_summaries)

    def test_data_contract_summary_can_create_serialized_output_of_summary(self):
        import pickle

        data_contract_summary = self._create_data_contract_summary(self.reference_dataframe_with_one_numerical_column)
        data_contract_summary.validate(
            self.dataframe_to_validate_with_one_numerical_column,
            self._create_formatted_report(self.reference_dataframe_with_one_numerical_column)
        )

        expected_data = {
            'attribute_summaries': {
                'feat_1': {
                    'expected_data_summary': {
                        'percentage_missing': 0.0,
                        'minimum': 1.0,
                        'maximum': 11.0
                    },
                    'actual_data_summary': {
                        'percentage_missing': 0.0,
                        'minimum': 1.0,
                        'maximum': 11.0
                    },
                    'binned_data': {
                        'bins': ['1.0-2.0', '2.0-3.0', '3.0-4.0', '4.0-5.0', '5.0-6.0', '6.0-7.0', '7.0-8.0', '8.0-9.0',
                                 '9.0-10.0', '10.0-11.0'],
                        'data': {
                            'expected_data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 21],
                            'actual_data': [11, 10, 9, 8, 7, 6, 5, 4, 3, 3]
                        }
                    }
                }
            },
            'num_critical_tests': 0
        }

        self.assertEqual(expected_data, pickle.loads(data_contract_summary.serialized_output()))
