"""
C`op`yright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class SchemaChecker(object):
    
    def __init__(self, column_names, column_types):
        self._reference_column_names = column_names.copy()
        self._column_types = column_types
        self._excluded_columns = []
        self._configured_columns = column_names.copy()

    def __str__(self):
        import json
        test_information = {
            'column_names': self._configured_columns,
            'column_types': self._column_types
        }
        return json.dumps(test_information)

    def configure(self, attributes):
        if isinstance(attributes, list):
            self._configured_columns =  self._union_of_column_names_preserving_order(self._configured_columns, attributes)
            for column in attributes:
                try:
                    self._excluded_columns.remove(column)
                except:
                    pass
        else:
            raise ValueError('Invalid option specified. Configure requires a list of column names')

    def exclude(self, attributes=None):
        if attributes == 'all':
            self._excluded_columns = self._configured_columns
            self._configured_columns = []
        elif isinstance(attributes, list):
            self._configured_columns = self._update_column_names_to_be_removed(self._configured_columns, attributes)
            self._excluded_columns = list(set(attributes).union(set(self._excluded_columns)))
        else:
            raise ValueError('Invalid option specified. Exclude requires a list of column names to be removed or "all" to exclue all columns')

    def validate(self, current_dataframe):
        import pandas

        current_df_columns, current_df_types = self._dataframe_statistics(current_dataframe)
        columns_to_validate = self._update_column_names_to_be_removed(current_df_columns, self._excluded_columns)
        types_to_validate = self._update_column_types(columns_to_validate, current_df_types)

        schema_check_results = {}
        if self._reference_column_names_match(columns_to_validate):
            if self._data_types_match(types_to_validate):
                schema_check_results['passed'] = True
                return schema_check_results

            schema_check_results['passed'] = False
            schema_check_results['error_message'] = 'column datatype mismatches'
            schema_check_results.update(self._type_mismatch_error_information(types_to_validate))
            return schema_check_results

        schema_check_results['passed'] = False

        current_column_names = set(columns_to_validate)

        if self._column_sets_not_equal(current_column_names):
            schema_check_results['error_message'] = 'column sets not equal'
            schema_check_results.update(self._column_sets_not_equal_error_information(current_column_names))
            return schema_check_results

        schema_check_results['error_message'] = 'columns not in order'

        ref_column_series = pandas.Series(self._configured_columns)
        current_column_series = pandas.Series(columns_to_validate)

        schema_check_results.update(self._column_sets_in_wrong_order_information(ref_column_series, current_column_series))
        return schema_check_results

    def _update_column_types(self, column_names, column_types):
        new_column_types = {}
        for columns in column_names:
            new_column_types[columns] = column_types[columns]
        return new_column_types

    def _update_column_names_to_be_removed(self, column_names, columns_to_be_removed):
        """
            removes the column listed in columns_to_be_removed while preserving the order
            of the column names in the column_names list.
            (NB The use of the set operation of list changes the order)
        """
        new_column_names = column_names.copy()
        for column in columns_to_be_removed:
            try:
                new_column_names.remove(column)
            except:
                pass
        return new_column_names

    def _union_of_column_names_preserving_order(self, column_names, columns_to_be_added):
        new_column_names = []
        for original_column in self._reference_column_names:
            if original_column in column_names or original_column in columns_to_be_added:
                new_column_names.append(original_column)
        return new_column_names

    def _reference_column_names_match(self, columns_to_validate):
        return self._configured_columns == columns_to_validate

    def _data_types_match(self, types_to_validate):
        bool_result = True
        for column, col_type in types_to_validate.items():
            try:
                bool_result = bool_result and self._column_types[column] == col_type
                if not bool_result:
                    return bool_result
            except:
                pass
        return bool_result

    def _column_sets_not_equal(self, current_column_names):
        return set(self._configured_columns) != current_column_names

    def _column_sets_not_equal_error_information(self, current_column_names):
        missing_in_ref = current_column_names - set(self._configured_columns)
        missing_in_current = set(self._configured_columns) - current_column_names

        return {'missing_in_ref': list(missing_in_ref), 'missing_in_current': list(missing_in_current)}

    @staticmethod
    def _column_sets_in_wrong_order_information(ref_column_series, current_column_series):
        columns_out_of_order = current_column_series[current_column_series != ref_column_series]
        return {'columns_out_of_order': list(columns_out_of_order)}

    def _type_mismatch_error_information(self, types_to_validate):
        mismatched_columns = {}

        for column_name in self._column_types.keys():
            ref_type = self._column_types[column_name]
            current_type = types_to_validate[column_name]

            if ref_type != current_type:
                mismatched_columns[column_name] = {
                    'ref_type': ref_type,
                    'current_type': current_type
                }

        return {'cols': mismatched_columns}

    @staticmethod
    def _dataframe_statistics(dataframe):
        column_names = list(dataframe.columns)
        column_types = {column_name: str(dataframe.dtypes[column_name]) for column_name in column_names}

        return column_names, column_types