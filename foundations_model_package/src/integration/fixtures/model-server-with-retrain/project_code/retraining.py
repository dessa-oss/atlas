import pickle
from datetime import datetime

def retrain(start_date, end_date):
    format_string = '%Y-%m-%dT%H:%M:%S'

    start_date = datetime.strptime(start_date, format_string)
    end_date = datetime.strptime(end_date, format_string)

    time_difference = (end_date - start_date).seconds

    with open('model_file', 'wb') as model_file:
        pickle.dump(time_difference, model_file)