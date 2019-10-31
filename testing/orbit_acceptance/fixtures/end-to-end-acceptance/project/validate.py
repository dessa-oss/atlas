from foundations_orbit import DataContract
import foundations
import pandas

reference_dataframe = pandas.read_pickle('reference_data.pkl')
contract = DataContract.load('.', 'test_data_contract_with_monitor')

validation_results = contract.validate(reference_dataframe, '2019-10-31')