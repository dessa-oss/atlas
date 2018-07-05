import pandas as pd
 
def create_data_frame():
    return pd.DataFrame([[index] for index in range(10)])

def scale_data(data, scale):
    scaled_data = data * scale
    return scaled_data, {'sum': scaled_data[0].sum()}
