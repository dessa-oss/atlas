"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit.contract_validators.schema_checker import SchemaChecker

class TestSchemaChecker(Spec):
    
    @let_now
    def empty_dataframe(self):
        import pandas
        return pandas.DataFrame()

    def test_check_schema_of_empty_dataframe_against_itself_passes(self):
        schema_checker = self._schema_checker_from_dataframe(self.empty_dataframe)
        column_names, column_types = self._dataframe_statistics(self.empty_dataframe)
        self.assertEqual({'passed': True}, schema_checker.schema_check_results(column_names, column_types))

    def _dataframe_statistics(self, dataframe):
        column_names = list(dataframe.columns)
        column_types = {column_name: str(dataframe.dtypes[column_name]) for column_name in column_names}

        return column_names, column_types
    
    def _schema_checker_from_dataframe(self, dataframe):
        column_names, column_types = self._dataframe_statistics(dataframe)
        return SchemaChecker(column_names, column_types)