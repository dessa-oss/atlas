import pandas as pd
 
def create_data_frame():
    return pd.DataFrame([range(10)])

def join_data(left, right):
    return pd.concat([left, right])
 
def print_it(data):
    print(data)