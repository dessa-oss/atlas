
from foundations_spec import *
from foundations_orbit.contract_validators.min_max_checker import MinMaxChecker

from hypothesis import given
import hypothesis.strategies as st
from hypothesis.extra.pandas import column, columns, data_frames
import numpy as np
import pandas as pd
# TODO: Refactor this whole thing to be cleaner
class TestMinMaxChecker(Spec):

    @let
    def column_name(self):
        return self.faker.word()

    @let
    def column_name_two(self):
        return self.faker.word()

    @let
    def column_name_three(self):
        return self.faker.word()

    @let
    def column_name_four(self):
        return self.faker.word()

    @let_now
    def dataframe_one_column(self):
        return pd.DataFrame(columns=[self.column_name], data=[20, 40, 50, 100, 110])

    @let_now
    def dataframe_two_columns(self):
        return pd.DataFrame(columns=[self.column_name, self.column_name_two], data=[[20, 0], [40, 4], [50, 10], [100, 40], [110, 99]])

    @let_now
    def dataframe_four_columns(self):
        return pd.DataFrame(columns=[self.column_name, self.column_name_two, self.column_name_three, self.column_name_four],
                                data=[[1, 5, 3, -1], [-1, 4, 2, -2], [-5, -1, 1, -4]])

    @let_now
    def dataframe_one_column_with_datetime(self):
        import datetime

        return pd.DataFrame(columns=[self.column_name], data=[datetime.datetime(2020,2,16), datetime.datetime(2018,2,16), datetime.datetime(2019,2,16)])

    @let
    def dataframe_one_column_reference_column_types(self):
        return {self.column_name: str(self.dataframe_one_column.iloc[:,0].dtype)}

    @let
    def dataframe_two_column_reference_column_types(self):
        return {self.column_name: str(self.dataframe_two_columns.iloc[:,0].dtype), self.column_name_two: str(self.dataframe_two_columns.iloc[:,1].dtype)}

    @let
    def dataframe_four_columns_column_types(self):
        return {self.column_name: str(self.dataframe_four_columns.iloc[:, 0].dtype),
                self.column_name_two: str(self.dataframe_four_columns.iloc[:, 1].dtype),
                self.column_name_three: str(self.dataframe_four_columns.iloc[:, 2].dtype),
                self.column_name_four: str(self.dataframe_four_columns.iloc[:, 3].dtype)}

    @let
    def dataframe_one_column_with_datetime_reference_column_types(self):
        return {self.column_name: str(self.dataframe_one_column_with_datetime.iloc[:,0].dtype)}

    def test_min_max_test_returns_empty_dictionary_when_checker_not_configured(self):
        min_max_checker = MinMaxChecker(self.dataframe_one_column_reference_column_types)
        result = min_max_checker.validate(self.dataframe_one_column)
        self.assertEqual({}, result)
    
    def test_min_max_test_raises_value_error_if_bounds_not_passed_and_columns_empty(self):
        min_max_checker = MinMaxChecker({})

        with self.assertRaises(ValueError) as error_context:
            min_max_checker.configure(attributes=[])

    def test_min_max_test_raises_value_error_if_bounds_not_passed(self):
        min_max_checker = MinMaxChecker({})

        with self.assertRaises(ValueError) as error_context:
            min_max_checker.configure(attributes=['abc'])
    
    def test_min_max_test_passes_when_lower_bound_provided(self):
        lower_bound = self.faker.random.randint(0, self.dataframe_one_column[self.column_name].min() - 1)
        min_max_checker = MinMaxChecker(self.dataframe_one_column_reference_column_types)
        min_max_checker.configure(attributes=[self.column_name], lower_bound=lower_bound)
        result = min_max_checker.validate(self.dataframe_one_column)

        expected_result = {
            self.column_name: {
                'min_test': {
                    'lower_bound': lower_bound,
                    'passed': True,
                    'min_value': 20
                }
            }
        }

        self.assertEqual(expected_result, result)

    def test_min_max_test_fails_when_lower_bound_provided_greater_than_min_value(self):
        lower_bound = 30
        min_max_checker = MinMaxChecker(self.dataframe_one_column_reference_column_types)
        min_max_checker.configure(attributes=[self.column_name], lower_bound=lower_bound)
        result = min_max_checker.validate(self.dataframe_one_column)

        expected_result = {
            self.column_name: {
                'min_test': {
                    'lower_bound': lower_bound,
                    'passed': False,
                    'min_value': 20,
                    'percentage_out_of_bounds': 0.2
                }
            }
        }

        self.assertEqual(expected_result, result)
    
    def test_min_max_test_passes_when_upper_bound_provided(self):
        max_val_of_dataframe = self.dataframe_one_column[self.column_name].max()
        upper_bound = self.faker.random.randint(max_val_of_dataframe + 1, max_val_of_dataframe + 100)
        min_max_checker = MinMaxChecker(self.dataframe_one_column_reference_column_types)
        min_max_checker.configure(attributes=[self.column_name], upper_bound=upper_bound)
        result = min_max_checker.validate(self.dataframe_one_column)

        expected_result = {
            self.column_name: {
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_of_dataframe
                }
            }
        }

        self.assertEqual(expected_result, result)

    
    def test_min_max_test_returns_empty_dict_with_empty_dataframe(self):

        min_max_checker = MinMaxChecker(self.dataframe_one_column_reference_column_types)
        min_max_checker.configure(attributes=[self.column_name], upper_bound=self.faker.random.randint(0,10))
        result = min_max_checker.validate(pd.DataFrame())

        expected_result = {}

        self.assertEqual(expected_result, result)

    def test_min_max_test_fails_when_upper_bound_provided_lesser_than_max_value(self):
        max_val_of_dataframe = self.dataframe_one_column[self.column_name].max()
        upper_bound = max_val_of_dataframe - 1
        min_max_checker = MinMaxChecker(self.dataframe_one_column_reference_column_types)
        min_max_checker.configure(attributes=[self.column_name], upper_bound=upper_bound)
        result = min_max_checker.validate(self.dataframe_one_column)

        expected_result = {
            self.column_name: {
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': False,
                    'max_value': max_val_of_dataframe,
                    'percentage_out_of_bounds': 0.2
                }
            }
        }

        self.assertEqual(expected_result, result)

    def test_min_max_test_runs_both_min_and_max_test_on_one_column_when_upper_bound_and_lower_bound_provided(self):
        min_val_of_dataframe = self.dataframe_one_column[self.column_name].min()
        max_val_of_dataframe = self.dataframe_one_column[self.column_name].max()

        lower_bound = self.faker.random.randint(0, min_val_of_dataframe - 1)
        upper_bound = self.faker.random.randint(max_val_of_dataframe + 1, max_val_of_dataframe + 100)

        min_max_checker = MinMaxChecker(self.dataframe_one_column_reference_column_types)
        min_max_checker.configure(attributes=[self.column_name], lower_bound=lower_bound, upper_bound=upper_bound)
        result = min_max_checker.validate(self.dataframe_one_column)

        expected_result = {
            self.column_name: {
                'min_test': {
                    'lower_bound': lower_bound,
                    'passed': True,
                    'min_value': min_val_of_dataframe,
                },
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_of_dataframe,
                }
            }
        }

        self.assertEqual(expected_result, result)

    def test_min_max_test_runs_min_test_and_passes_on_two_columns(self):
        min_val_one = self.dataframe_two_columns[self.column_name].min()
        min_val_two = self.dataframe_two_columns[self.column_name_two].min()

        min_val_of_dataframes = min(min_val_one, min_val_two)
        lower_bound = min_val_of_dataframes - 1

        min_max_checker = MinMaxChecker(self.dataframe_two_column_reference_column_types)
        min_max_checker.configure(attributes=[self.column_name, self.column_name_two], lower_bound=lower_bound)
        result = min_max_checker.validate(self.dataframe_two_columns)

        expected_result = {
            self.column_name: {
                'min_test': {
                    'lower_bound': lower_bound,
                    'passed': True,
                    'min_value': min_val_one,
                },
            },
            self.column_name_two: {
                'min_test': {
                    'lower_bound': lower_bound,
                    'passed': True,
                    'min_value': min_val_two,
                },
            }
        }

        self.assertEqual(expected_result, result)
    
    def test_min_max_test_runs_max_test_and_passes_on_two_columns(self):
        max_val_one = self.dataframe_two_columns[self.column_name].max()
        max_val_two = self.dataframe_two_columns[self.column_name_two].max()

        max_val_of_dataframes = max(max_val_one, max_val_two)
        upper_bound = max_val_of_dataframes + 1

        min_max_checker = MinMaxChecker(self.dataframe_two_column_reference_column_types)
        min_max_checker.configure(attributes=[self.column_name, self.column_name_two], upper_bound=upper_bound)
        result = min_max_checker.validate(self.dataframe_two_columns)

        expected_result = {
            self.column_name: {
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_one,
                },
            },
            self.column_name_two: {
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_two,
                },
            }
        }

        self.assertEqual(expected_result, result)

    def test_min_max_test_with_multiple_configure_statements_returns_expected_data(self):
        max_val_one = self.dataframe_two_columns[self.column_name].max()
        min_val_two = self.dataframe_two_columns[self.column_name_two].min()

        upper_bound = max_val_one + 1
        lower_bound = min_val_two - 1

        min_max_checker = MinMaxChecker(self.dataframe_two_column_reference_column_types)
        min_max_checker.configure(attributes=[self.column_name], upper_bound=upper_bound)
        min_max_checker.configure(attributes=[self.column_name_two], lower_bound=lower_bound)
        
        result = min_max_checker.validate(self.dataframe_two_columns)

        expected_result = {
            self.column_name: {
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_one,
                },
            },
            self.column_name_two: {
                'min_test': {
                    'lower_bound': lower_bound,
                    'passed': True,
                    'min_value': min_val_two,
                },
            }
        }

        self.assertEqual(expected_result, result)
    
    def test_min_max_test_with_configure_on_same_column_twice_overwrites_test(self):
        max_val_one = self.dataframe_two_columns[self.column_name].max()

        upper_bound = max_val_one + 1

        min_max_checker = MinMaxChecker(self.dataframe_two_column_reference_column_types)
        min_max_checker.configure(attributes=[self.column_name], lower_bound=100)
        min_max_checker.configure(attributes=[self.column_name], upper_bound=upper_bound)
        
        result = min_max_checker.validate(self.dataframe_two_columns)

        expected_result = {
            self.column_name: {
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_one,
                },
            },
        }

        self.assertEqual(expected_result, result)

    def test_min_max_test_with_both_max_and_min_tests_on_two_columns(self):
        max_val_one = self.dataframe_two_columns[self.column_name].max()
        max_val_two = self.dataframe_two_columns[self.column_name_two].max()
        min_val_one = self.dataframe_two_columns[self.column_name].min()
        min_val_two = self.dataframe_two_columns[self.column_name_two].min()

        upper_bound_one = max_val_one + 1
        lower_bound_one = min_val_one - 1
        upper_bound_two = max_val_two + 1
        lower_bound_two = min_val_two - 1

        min_max_checker = MinMaxChecker(self.dataframe_two_column_reference_column_types)
        min_max_checker.configure(attributes=[self.column_name], lower_bound=lower_bound_one, upper_bound=upper_bound_one)
        min_max_checker.configure(attributes=[self.column_name_two], lower_bound=lower_bound_two, upper_bound=upper_bound_two)
        
        result = min_max_checker.validate(self.dataframe_two_columns)

        expected_result = {
            self.column_name: {
                'min_test': {
                    'lower_bound': lower_bound_one,
                    'passed': True,
                    'min_value': min_val_one,
                },
                'max_test': {
                    'upper_bound': upper_bound_one,
                    'passed': True,
                    'max_value': max_val_one,
                },
            },
            self.column_name_two: {
                'min_test': {
                    'lower_bound': lower_bound_two,
                    'passed': True,
                    'min_value': min_val_two,
                },
                'max_test': {
                    'upper_bound': upper_bound_two,
                    'passed': True,
                    'max_value': max_val_two,
                },
            }
        }

        self.assertEqual(expected_result, result)
    
    def test_min_max_test_excluding_all_columns(self):
        min_max_checker = MinMaxChecker(self.dataframe_two_column_reference_column_types)
        min_max_checker.configure(attributes=[self.column_name, self.column_name_two], lower_bound=0)
        min_max_checker.exclude(attributes='all')
        
        result = min_max_checker.validate(self.dataframe_two_columns)

        expected_result = {}

        self.assertEqual(expected_result, result)

    def test_min_max_test_excluding_one_column(self):
        max_val_one = self.dataframe_two_columns[self.column_name].max()

        upper_bound = max_val_one + 1

        min_max_checker = MinMaxChecker(self.dataframe_two_column_reference_column_types)
        min_max_checker.configure(attributes=[self.column_name, self.column_name_two], upper_bound=upper_bound)
        min_max_checker.exclude([self.column_name_two])

        result = min_max_checker.validate(self.dataframe_two_columns)

        expected_result = {
            self.column_name: {
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_one,
                },
            },
        }

        self.assertEqual(expected_result, result)
    
    def test_min_max_test_with_one_column_datetime(self):
        import datetime
        max_val_one = self.dataframe_one_column_with_datetime[self.column_name].max()
        min_val_one = self.dataframe_one_column_with_datetime[self.column_name].min() 

        upper_bound = max_val_one + datetime.timedelta(days=1)
        lower_bound = min_val_one + datetime.timedelta(days=1)

        min_max_checker = MinMaxChecker(self.dataframe_one_column_with_datetime_reference_column_types)
        min_max_checker.configure(attributes=[self.column_name], lower_bound=lower_bound, upper_bound=upper_bound)
        
        result = min_max_checker.validate(self.dataframe_one_column_with_datetime)

        expected_result = {
            self.column_name: {
                'min_test': {
                    'lower_bound': lower_bound,
                    'passed': False,
                    'min_value': min_val_one,
                    'percentage_out_of_bounds': 0.333
                },
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_one,
                }
            }
        }

        self.assertEqual(expected_result, result)

    def test_min_max_checker_has_to_string(self):
        min_max_checker = MinMaxChecker(self.dataframe_two_column_reference_column_types)
        min_max_checker.configure(attributes=[self.column_name], lower_bound=0, upper_bound=50)
        min_max_checker.configure(attributes=[self.column_name_two], lower_bound=20, upper_bound=70)


        expected_output = {
            self.column_name: {
                'lower_bound': 0,
                'upper_bound': 50
            },
            self.column_name_two: {
                'lower_bound': 20,
                'upper_bound': 70
            },
        }
        self.assertEqual(str(expected_output), str(min_max_checker))

    def test_min_max_checker_has_info_dict(self):
        min_max_checker = MinMaxChecker(self.dataframe_two_column_reference_column_types)
        min_max_checker.configure(attributes=[self.column_name], lower_bound=0, upper_bound=50)
        min_max_checker.configure(attributes=[self.column_name_two], lower_bound=20, upper_bound=70)

        expected_output = {
            self.column_name: {
                'lower_bound': 0,
                'upper_bound': 50
            },
            self.column_name_two: {
                'lower_bound': 20,
                'upper_bound': 70
            },
        }
        self.assertEqual(expected_output, min_max_checker.info())

    def test_min_max_checker_configure_fails_when_reference_dataframe_with_bool_types_used(self):

        reference_column_types = {self.column_name: 'int64', self.column_name_two: 'bool'}
        min_max_checker = MinMaxChecker(reference_column_types)

        expected_error_dictionary = {
            self.column_name_two: 'bool'
        }
        with self.assertRaises(ValueError) as e:
            min_max_checker.configure(attributes=[self.column_name, self.column_name_two], lower_bound=0)

        self.assertEqual(f'The following columns have invalid types: {expected_error_dictionary}', e.exception.args[0])

    def test_min_max_checker_when_configure_fails_then_no_columns_are_configured(self):

        reference_column_types = self.dataframe_one_column_with_datetime_reference_column_types
        reference_column_types[self.column_name_two] = 'object'
        min_max_checker = MinMaxChecker(reference_column_types)

        try:
            min_max_checker.configure(attributes=[self.column_name, self.column_name_two], lower_bound=50, upper_bound=100)
        except:
            self.assertEqual('{}', str(min_max_checker))


    def test_min_max_checker_configure_fails_when_reference_dataframe_with_multiple_unsumpported_types_used(self):

        reference_column_types = {self.column_name: 'str', self.column_name_two: 'bool'}
        min_max_checker = MinMaxChecker(reference_column_types)

        expected_error_dictionary = {
            self.column_name: 'str',
            self.column_name_two: 'bool'
        }

        with self.assertRaises(ValueError) as e:
            min_max_checker.configure(attributes=[self.column_name, self.column_name_two], lower_bound=0)

        self.assertEqual(f'The following columns have invalid types: {expected_error_dictionary}', e.exception.args[0])

    def test_min_max_checker_with_zero_lower_bound_and_zero_upper_bound(self):
        max_val_one = self.dataframe_four_columns[self.column_name].max()
        max_val_two = self.dataframe_four_columns[self.column_name_two].max()
        max_val_three = self.dataframe_four_columns[self.column_name_three].max()
        max_val_four = self.dataframe_four_columns[self.column_name_four].max()
        min_val_one = self.dataframe_four_columns[self.column_name].min()
        min_val_two = self.dataframe_four_columns[self.column_name_two].min()
        min_val_three = self.dataframe_four_columns[self.column_name_three].min()
        min_val_four = self.dataframe_four_columns[self.column_name_four].min()

        upper_bound_one = 0
        lower_bound_one = -6
        upper_bound_two = 4
        lower_bound_two = 0
        upper_bound_three = 7
        lower_bound_three = 0
        upper_bound_four = 0
        lower_bound_four = -3

        min_max_checker = MinMaxChecker(self.dataframe_four_columns_column_types)
        min_max_checker.configure(attributes=[self.column_name], lower_bound=lower_bound_one, upper_bound=upper_bound_one)
        min_max_checker.configure(attributes=[self.column_name_two], lower_bound=lower_bound_two,
                                  upper_bound=upper_bound_two)
        min_max_checker.configure(attributes=[self.column_name_three], lower_bound=lower_bound_three,
                                  upper_bound=upper_bound_three)
        min_max_checker.configure(attributes=[self.column_name_four], lower_bound=lower_bound_four,
                                  upper_bound=upper_bound_four)

        result = min_max_checker.validate(self.dataframe_four_columns)

        expected_result = {
            self.column_name: {
                'min_test': {
                    'lower_bound': lower_bound_one,
                    'passed': True,
                    'min_value': min_val_one,
                },
                'max_test': {
                    'upper_bound': upper_bound_one,
                    'passed': False,
                    'max_value': max_val_one,
                    'percentage_out_of_bounds': 0.333
                },
            },
            self.column_name_two: {
                'min_test': {
                    'lower_bound': lower_bound_two,
                    'passed': False,
                    'min_value': min_val_two,
                    'percentage_out_of_bounds': 0.333
                },
                'max_test': {
                    'upper_bound': upper_bound_two,
                    'passed': False,
                    'max_value': max_val_two,
                    'percentage_out_of_bounds': 0.333
                },
            },
            self.column_name_three: {
                'min_test': {
                    'lower_bound': lower_bound_three,
                    'passed': True,
                    'min_value': min_val_three,
                },
                'max_test': {
                    'upper_bound': upper_bound_three,
                    'passed': True,
                    'max_value': max_val_three,
                },
            },
            self.column_name_four: {
                'min_test': {
                    'lower_bound': lower_bound_four,
                    'passed': False,
                    'min_value': min_val_four,
                    'percentage_out_of_bounds': 0.333
                },
                'max_test': {
                    'upper_bound': upper_bound_four,
                    'passed': True,
                    'max_value': max_val_four,
                },
            }
        }

        self.assertEqual(expected_result, result)

    @st.composite
    def dataframes(draw, *strategies: st.SearchStrategy) -> st.SearchStrategy:
        names = draw(st.lists(st.integers(), unique=True, min_size=1))
        cols = [column(name, elements=draw(st.sampled_from(strategies))) for name in names]
        return draw(data_frames(cols))

    # TODO Temporarily restrict from using NaNs
    @given(dataframes(st.integers(), st.floats(allow_nan=False)))
    def test_min_max(self, df: pd.DataFrame) -> None:
        min_max = MinMaxChecker({col_name: "int" for col_name in df.columns})
        if df.empty:
            min_max.configure(df.columns, lower_bound=0, upper_bound=1)
            self.assertEqual({}, min_max.validate(df))
        else:
            min_bound = min(df[col].min() for col in df.columns)
            max_bound = max(df[col].max() for col in df.columns)
            min_max.configure(df.columns, lower_bound=min_bound, upper_bound=max_bound)
            report = min_max.validate(df)
            expected = {
                col: {
                    "max_test": {
                        "max_value": df[col].max(),
                        "passed": True,
                        "upper_bound": max_bound,
                    },
                    "min_test": {
                        "min_value": df[col].min(),
                        "passed": True,
                        "lower_bound": min_bound,
                    },
                }
                for col in df.columns
            }
            self.assertEqual(report, expected)
