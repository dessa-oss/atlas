"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
A utility class which can create a one-hot encoding as well as fit a dataframe
to it later.
"""

class OneHotEncoder(object):
    def __init__(self):
        self._allowed_values = {}

    def fit(self, data_frame):
        for column in data_frame:
            self._allowed_values[column] = data_frame[column].unique()
        return self

    def transform(self, data_frame):
        from common.prep import get_mode, impute_for_one_hot, one_hot_encode

        for column in data_frame:
            values = self._allowed_values[column]
            mode = get_mode(data_frame, column)
            data_frame = impute_for_one_hot(data_frame, column, values, mode)
            data_frame = one_hot_encode(data_frame, column)
            
            for value in values:
                encoded_column = '{}_{}'.format(column, value)
                if not encoded_column in data_frame:
                    data_frame[encoded_column] = 0
        
        return data_frame
