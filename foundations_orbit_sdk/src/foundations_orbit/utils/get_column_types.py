"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 06 2018
"""


def get_column_types(dataframe):
        from pandas.api.types import is_string_dtype, is_bool_dtype, is_datetime64_any_dtype

        column_names = list(dataframe.columns)
        column_types = {column_name: str(dataframe.dtypes[column_name]) for column_name in column_names}
        object_column_names = list(dataframe.dtypes[dataframe.dtypes == 'object'].index)

        for col_name in object_column_names:
            object_type_column = dataframe[col_name]
            if _column_has_nans(object_type_column):
                object_type_column = _filter_nans_from_column(object_type_column)

            if is_string_dtype(object_type_column):
                column_types[col_name] = 'str'
            elif is_datetime64_any_dtype(object_type_column):
                column_types[col_name] = 'datetime'
            elif is_bool_dtype(object_type_column):
                column_types[col_name] = 'bool'

        return column_names, column_types


def _column_has_nans(column):
    return column.isna().sum()

def _filter_nans_from_column(column):
    return column[~column.isna()]
