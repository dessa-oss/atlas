from datetime import datetime

from foundations_orbit import DataContract
import foundations
import pandas as pd

ref_dataframe = pd.DataFrame(data={'col1': [1,2,3,4,5]})
cur_dataframe = pd.DataFrame(data={'col1': [2,3,4,5,6]})
contract = DataContract('my_data_contract', ref_dataframe)

validation_results = contract.validate(cur_dataframe, '2019-10-31')
foundations.track_production_metrics('metric', {str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')): 2})
