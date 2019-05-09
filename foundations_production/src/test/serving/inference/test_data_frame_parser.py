"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from foundations_spec import *
from pandas.testing import assert_frame_equal
from pandas import DataFrame
from foundations_production.serving.inference.data_frame_parser import DataFrameParser

class TestDataFrameParser(Spec):
    
    @let
    def parser(self):
        return DataFrameParser()
    
    def test_data_frame_for_returns_an_empty_data_frame(self):
        input = {'rows': [], 'schema': []}
        expected_data_frame = DataFrame([])
        assert_frame_equal(expected_data_frame, self.parser.data_frame_for(input))

    def test_data_frame_for_returns_data_frame_for_single_row_and_column(self):
        input = {'rows': [['some value']], 'schema': [{'name': 'first column', 'type': 'str'}]}
        expected_data_frame = DataFrame([{'first column': 'some value'}])
        assert_frame_equal(expected_data_frame, self.parser.data_frame_for(input))

    def test_data_frame_for_returns_data_frame_for_mutiple_rows_and_columns(self):
        input = {'rows': [['value', 43234], ['spider', 323]], 'schema': [{'name': '1st column', 'type': 'string'}, {'name': '2nd column', 'type': 'int'}]}
        expected_data_frame = DataFrame([{'1st column': 'value', '2nd column': 43234}, {'1st column': 'spider', '2nd column': 323}])
        assert_frame_equal(expected_data_frame, self.parser.data_frame_for(input))
