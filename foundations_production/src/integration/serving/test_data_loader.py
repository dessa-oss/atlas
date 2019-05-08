"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.serving.data_loader import DataLoader

class TestDataLoader(Spec):

    @set_up
    def set_up(self):
        self._create_local_dataframe()

    @tear_down
    def tear_down(self):
        import os
        os.remove(self.file_name)

    @let
    def file_name_with_scheme(self):
        return 'local://' + self.file_name

    @let
    def file_name(self):
        return '/tmp/load_job.pkl'

    @let
    def features(self):
        import pandas

        features = pandas.DataFrame({
            'Sex': [1, 5],
            'Cabin': [1, 0],
            'Fare': [15, -100],
        })
        
        return features

    def test_data_loader_loads_local_file(self):
        from pandas.testing import assert_frame_equal

        data_loader = DataLoader()
        dataframe = data_loader.load_data(self.file_name_with_scheme)

        assert_frame_equal(self.features, dataframe)
        

    def _create_local_dataframe(self):
        self._save_dataframe(self.features, self.file_name)
        
    def _save_dataframe(self, dataframe, file_name):
        import pickle

        with open(file_name, 'wb') as dataframe_file:
            pickle.dump(dataframe, dataframe_file)
        