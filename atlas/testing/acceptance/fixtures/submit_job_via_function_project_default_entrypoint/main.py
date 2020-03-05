
import foundations
import json

params = foundations.load_parameters()
foundations.log_metric('how_i_lern', params['learning_rate'])
foundations.log_metric('first_boi', params['layers'][0]['neurons'])
foundations.log_metric('second_boi', params['layers'][1]['neurons'])