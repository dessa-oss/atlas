"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

def make_data(data='created some data here'):
    return data

def divide_by_zero():
    return 1 / 0

def empty_dataframe():
    import pandas as pd
    return pd.DataFrame()

def get_asdf(df):
    return df["asdf"]

def implicit_chained_exception():
    try:
        1 / 0
    except:
        return {}["asdf"]

def explicit_chained_exception():
    try:
        1 / 0
    except Exception as ex:
        raise TypeError() from ex