"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import fakeredis
from foundations_orbit.data_contract import DataContract

# A hack so that we can use execute command with our out of date fakeredis
def do_nothing(*args):
    return
fake_redis = fakeredis.FakeRedis()
fake_redis.execute_command = do_nothing

class TestDataContractCategorizer(Spec):
    mock_open = let_patch_mock_with_conditional_return('builtins.open')
    mock_file_for_write = let_mock()
    mock_file_for_read = let_mock()

    @let
    def contract_name(self):
        return self.faker.word()

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def model_name(self):
        return self.faker.word()

    @let
    def monitor_package_directory(self):
        return self.faker.file_path()

    @let
    def data_contract_file_path(self):
        return f'{self.monitor_package_directory}/{self.contract_name}.pkl'

    @let
    def column_name_1(self):
        return self.faker.word()
    
    @let
    def column_name_2(self):
        return self.faker.word()

    @let
    def column_name_3(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        self.mock_file_for_write.__enter__ = lambda *args: self.mock_file_for_write
        self.mock_file_for_write.__exit__ = lambda *args: None

        self.mock_file_for_read.__enter__ = lambda *args: self.mock_file_for_read
        self.mock_file_for_read.__exit__ = lambda *args: None

        self.mock_open.return_when(self.mock_file_for_write, self.data_contract_file_path, 'wb')
        self.mock_open.return_when(self.mock_file_for_read, self.data_contract_file_path, 'rb')

        mock_environ = self.patch('os.environ', {})
        mock_environ['PROJECT_NAME'] = self.project_name
        mock_environ['MONITOR_NAME'] = self.model_name

        def do_nothing(*args):
            return
        fake_redis = fakeredis.FakeRedis()
        fake_redis.execute_command = do_nothing
        self._redis = self.patch('foundations_contrib.global_state.redis_connection', fake_redis)

    @tear_down
    def tear_down(self):
        self._redis.flushall()

    def test_data_contract_categorizer_for_numerical_returns_correct_dicitonary(self):
        import numpy, pandas

        data = {
            self.column_name_1: list(numpy.random.randn(100)),
            self.column_name_2: list(numpy.random.choice([1,2,3,4,5], 100)),
            self.column_name_3: [1,2,3,4,5,6,7,8,9,10,11] + [1]*89
        }

        dataframe = pandas.DataFrame(data)
        contract = DataContract(self.contract_name, dataframe)

        expected_attribute_categories = {
            self.column_name_1: False,
            self.column_name_2: True,
            self.column_name_3: False
        }

        self.assertEqual(expected_attribute_categories, contract._categorical_attributes)

    def test_data_contract_categorizer_for_string_returns_correct_dicitonary(self):
        import numpy, pandas

        data = {
            self.column_name_1: list(numpy.random.choice([self.faker.word(), self.faker.word(), self.faker.word()], 100)),
            self.column_name_2: [self.faker.word() for _ in range(80)] + [self.faker.word()]*20
        }


        dataframe = pandas.DataFrame(data)
        contract = DataContract(self.contract_name, dataframe)

        expected_attribute_categories = {
            self.column_name_1: True,
            self.column_name_2: False
        }

        self.assertEqual(expected_attribute_categories, contract._categorical_attributes)

    def test_data_contract_categorizer_for_bool_returns_correct_dicitonary(self):
        import numpy, pandas

        data = {
            self.column_name_1: list(numpy.random.choice([True, False], 100))
        }

        dataframe = pandas.DataFrame(data)
        contract = DataContract(self.contract_name, dataframe)

        expected_attribute_categories = {
            self.column_name_1: True,
        }

        self.assertEqual(expected_attribute_categories, contract._categorical_attributes)


    def test_data_contract_categorizer_for_datetime_returns_correct_dicitonary(self):
        import numpy, pandas

        data = {
            self.column_name_1: list(numpy.random.choice([self.faker.date_time() for _ in range(5)], 100)),
            self.column_name_2: [self.faker.date_time() for _ in range(80)] + [self.faker.date_time()]*20
        }

        dataframe = pandas.DataFrame(data)
        contract = DataContract(self.contract_name, dataframe)

        expected_attribute_categories = {
            self.column_name_1: True,
            self.column_name_2: False
        }

        self.assertEqual(expected_attribute_categories, contract._categorical_attributes)

    def test_data_contract_uses_categorical_logic_for_distribution_check(self):
        import numpy, pandas

        dataframe = pandas.DataFrame({self.column_name_1: [1,1,1, 2,2,2, 3,3,3, 4,4,4]})
        current_dataframe = pandas.DataFrame({self.column_name_1: [1,1, 2,2, 3,3, 4,4, 5,5,5,5]})
        contract = DataContract(self.contract_name, dataframe)

        validation_report = contract.validate(current_dataframe)
        dist_check_report = validation_report['dist_check_results']

        expected_report = {
            self.column_name_1: {
                'binned_l_infinity':  0.333,
                'binned_passed': False
            }
        }

        self.assertEqual(expected_report, dist_check_report)

    
    def test_data_contract_ignores_non_categorical_string_column(self):
        import numpy, pandas

        dataframe = pandas.DataFrame({self.column_name_1: [self.faker.word() for _ in range(20)]})
        contract = DataContract(self.contract_name, dataframe)

        validation_report = contract.validate(dataframe)
        dist_check_report = validation_report['dist_check_results']

        expected_report = {
            self.column_name_1: {
                'message': 'non-categorical strings are not supported',
                'binned_passed': None,
            }
        }

        self.assertEqual(expected_report, dist_check_report)
    

    def test_data_contract_uses_categorical_logic_for_distribution_check(self):
        import numpy, pandas

        dataframe = pandas.DataFrame({self.column_name_1: ['a']*3 + ['b']*3 + ['c']*3 + ['d']*3})
        current_dataframe = pandas.DataFrame({self.column_name_1: ['a','a','b','b','c','c','d','d'] + ['e']*4})
        contract = DataContract(self.contract_name, dataframe)

        validation_report = contract.validate(current_dataframe)
        dist_check_report = validation_report['dist_check_results']

        expected_report = {
            self.column_name_1: {
                'binned_l_infinity':  0.333,
                'binned_passed': False
            }
        }

        self.assertEqual(expected_report, dist_check_report)
    
    def test_data_contract_passes_when_same_dataframe_used_with_bools(self):
        import numpy, pandas

        dataframe = pandas.DataFrame({self.column_name_1: [self.faker.pybool() for _ in range(12)]})
        current_dataframe = dataframe
        contract = DataContract(self.contract_name, dataframe)

        validation_report = contract.validate(current_dataframe)
        dist_check_report = validation_report['dist_check_results']

        expected_report = {
            self.column_name_1: {
                'binned_l_infinity':  0.0,
                'binned_passed': True
            }
        }

        self.assertEqual(expected_report, dist_check_report)


    def test_data_contract_passes_when_different_dataframe_used_with_bools(self):
        import numpy, pandas

        dataframe = pandas.DataFrame({self.column_name_1: [True, False, True, True]})
        current_dataframe = pandas.DataFrame({self.column_name_1: [True, False, False, True]})
        contract = DataContract(self.contract_name, dataframe)

        validation_report = contract.validate(current_dataframe)
        dist_check_report = validation_report['dist_check_results']

        expected_report = {
            self.column_name_1: {
                'binned_l_infinity':  0.25,
                'binned_passed': False
            }
        }

        self.assertEqual(expected_report, dist_check_report)


    def test_data_contract_passes_when_same_dataframe_used_with_datetime(self):
        import numpy, pandas, datetime

        dataframe = pandas.DataFrame({self.column_name_1: [self.faker.date_time() for _ in range(100)]})
        current_dataframe = dataframe
        contract = DataContract(self.contract_name, dataframe)

        validation_report = contract.validate(current_dataframe)
        dist_check_report = validation_report['dist_check_results']

        expected_report = {
            self.column_name_1: {
                'binned_l_infinity':  0.0,
                'binned_passed': True
            }
        }

        self.assertEqual(expected_report, dist_check_report)


    def test_data_contract_uses_categorical_logic_for_distribution_check_with_datetime(self):
        import numpy, pandas
        a,b,c,d = self.faker.date_time(), self.faker.date_time(), self.faker.date_time(), self.faker.date_time()
        dataframe = pandas.DataFrame({self.column_name_1: [a]*10 + [b]*10 + [c]*10 + [d]*10})
        current_dataframe = pandas.DataFrame({self.column_name_1: [a]*5 + [b]*5 + [c]*5 + [d]*5 + [self.faker.date_time()]*20})
        contract = DataContract(self.contract_name, dataframe)

        validation_report = contract.validate(current_dataframe)
        dist_check_report = validation_report['dist_check_results']

        expected_report = {
            self.column_name_1: {
                'binned_l_infinity':  0.5,
                'binned_passed': False
            }
        }

        self.assertEqual(expected_report, dist_check_report)

    
    def test_data_contract_uses_non_categorical_logic_for_distribution_check_with_datetime(self):
        import pandas, datetime
        a,b,c,d = self.faker.date_time(), self.faker.date_time(), self.faker.date_time(), self.faker.date_time()
        dataframe = pandas.DataFrame({self.column_name_1: [a]*3 + [b]*3 + [c]*3 + [d]*3})
        current_dataframe = pandas.DataFrame({self.column_name_1: [a]*2 + [b]*2 + [c]*2 + [d]*2 + [max(a,b,c,d) + datetime.timedelta(10)]*4})
        contract = DataContract(self.contract_name, dataframe)

        validation_report = contract.validate(current_dataframe)
        dist_check_report = validation_report['dist_check_results']

        expected_report = {
            self.column_name_1: {
                'binned_l_infinity':  0.25,
                'binned_passed': False
            }
        }

        self.assertEqual(expected_report, dist_check_report)