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
    def empty_schema(self):
        return []

    @let
    def empty_rows(self):
        return []

    @let
    def parser(self):
        return DataFrameParser()
    
    def test_data_frame_for_returns_an_empty_data_frame(self):
        input = {'rows': self.empty_rows, 'schema': self.empty_schema}
        expected_data_frame = DataFrame([])
        assert_frame_equal(expected_data_frame, self.parser.data_frame_for(input))

    