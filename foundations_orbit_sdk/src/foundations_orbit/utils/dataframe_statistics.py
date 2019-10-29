"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 06 2018
"""


def dataframe_statistics(dataframe):
        import numpy
        import datetime
        column_names = list(dataframe.columns)
        column_types = {column_name: str(dataframe.dtypes[column_name]) for column_name in column_names}
        number_of_rows = len(dataframe)

        for col_name, col_type in column_types.items():
            if col_type == "object":
                object_type_column = dataframe[col_name]
                string_column_mask = ['str' in str(type(value)) or value != value for value in object_type_column]
                date_column_mask = [type(value) == datetime or value != value for value in object_type_column]
                bool_column_mask = [type(value) == bool or value != value for value in object_type_column]
                if all(string_column_mask):
                    column_types[col_name] = 'str'
                elif all(date_column_mask):
                    column_types[col_name] = 'datetime'
                elif all(bool_column_mask):
                    column_types[col_name] = 'bool'
                

        return column_names, column_types, number_of_rows
