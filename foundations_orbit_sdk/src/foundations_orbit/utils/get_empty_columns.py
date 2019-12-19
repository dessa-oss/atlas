"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 06 2018
"""

def get_empty_columns(col_names, col_types, dataframe):
    float_columns = [col_name for col_name, col_type in col_types.items() if col_type == 'float64']
    empty_columns = []

    for col_name in float_columns:
        if dataframe[col_name].isna().sum() / len(dataframe) == 1.0:
            col_types[col_name] = 'empty'
            empty_columns.append(col_name)

    col_names = [column for column in col_names if column not in empty_columns]

    return col_names, col_types, empty_columns
