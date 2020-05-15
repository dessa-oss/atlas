
import foundations
from foundations import set_tag
from foundations_contrib.global_state import current_foundations_job

from model import *

set_tag('model', 'cnn')

def print_words():
    print(f'Job \'{current_foundations_job().job_id}\' deployed')
    print('Hello World!')

print_words()

addition_result = add(82,2)
set_tag('Loss', addition_result)

subtraction_result = subtract(44,2)
foundations.log_metric('Accuracy', subtraction_result)
