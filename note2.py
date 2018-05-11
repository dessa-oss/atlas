# reading
# we need a system for understanding results, allowing the user to query and compare different types of metrics from many models

# gets all results....ever
result_reader = ResultReader()

# result reader to data_frame will return a data_frame from all results from every experiment
data_frame = result_reader.to_data_frame()
data_frame['roc_auc'].mean()


# at BNS they got all results, all the time
# we need to figure out a system to filter this