
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
        import sys

        if sys.version_info.major < 3:
            exec("raise TypeError('python 2')")
        else:
            exec("raise TypeError() from ex")