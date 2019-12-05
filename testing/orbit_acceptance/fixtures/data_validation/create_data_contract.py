from foundations_orbit import DataContract
import numpy
import pandas

numpy.random.seed(42)

contract_name = 'dv_contract'
reference_dataframe = pandas.DataFrame(numpy.random.uniform(-1, 1, size=(100, 2)), columns=['feat_1', 'feat_2'])

data_contract = DataContract(contract_name, df=reference_dataframe)
data_contract.special_value_test.configure(attributes=['feat_1', 'feat_2'], thresholds={numpy.nan: 0.1})
data_contract.save('/tmp')
