"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""


class DataFrameParser(object):
    
    def data_frame_for(self, input):
        from pandas import DataFrame

        columns = self._data_frame_columns(input)
        return DataFrame(input['rows'], columns=columns)

    def data_frame_as_json(self, input):
        schema = []
        for column_name in input:
            column_data_type = str(input[column_name].dtype)
            schema.append({
                'name': column_name,
                'type': column_data_type
            })
        
        rows = input.values.tolist()
        return {'rows': rows, 'schema': schema}

    def _data_frame_columns(self, input):
        return [field['name'] for field in input['schema']]

