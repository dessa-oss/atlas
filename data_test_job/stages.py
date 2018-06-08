def load_data(path):
    from pandas import read_csv

    log().debug('Begin loading %s', '/home/thomas/Documents/test_data/Resources.csv')
    return read_csv(path)

def describe(data_frame):
    description = data_frame.describe().to_dict()
    return data_frame, {'description': description}

def log():
    from vcat import log_manager
    return log_manager.get_logger(__name__)
