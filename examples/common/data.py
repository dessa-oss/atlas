"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
Though data loading is just another step in a job, it could be useful for the MLE
to separate and collect common functionalities in appropriate files.

This one just loads the titanic dataset from the appropriate csv and returns it as
a pandas dataframe.
"""

import pandas as pd


def load_titanic():
    return pd.read_csv('titanic.csv')
