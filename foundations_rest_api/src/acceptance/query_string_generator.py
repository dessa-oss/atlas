"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

class QueryStringGenerator(object):

    def sort_column(self, column, descending=True):
        sign = '-' if descending else ''
        return '?sort={}{}'.format(sign, column)

    def sort_all_columns(self, columns, descending=True):
        param_value = ','.join([('-' if descending else '') + column for column in columns])
        return '?sort=' + param_value

    def sort_alternation(self, columns):

        def prefix_column(index, column):
            return column if index % 2 == 0 else '-{}'.format(column)

        prefixed_columns = [prefix_column(*item) for item in enumerate(columns)]
        param_value = ','.join(prefixed_columns)
        return '?sort=' + param_value

    def filter_range(self, column_data):
        column_name = column_data['name']
        start_param, end_param =  column_data['test_values']
        return '?{}_starts={}&{}_ends={}'.format(column_name, start_param, column_name, end_param)

    def filter_exact_match_one_option(self, column_data):
        column_name = column_data['name']
        param_value = column_data['test_values'][0]
        return '?{}={}'.format(column_name, param_value)

    def filter_exact_match_two_options(self, column_data):
        column_name = column_data['name']
        start_param, end_param =  column_data['test_values']
        return '?{}={},{}'.format(column_name, start_param, end_param)
