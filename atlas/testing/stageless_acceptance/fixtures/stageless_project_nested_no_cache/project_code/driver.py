
import foundations
from foundations import set_tag

from model import *

set_tag('model', 'cnn')

def print_words():
    print('Hello World!')

print_words()

addition_result = add(82,2)
set_tag('Loss', addition_result)

subtraction_result = subtract(44,2)
foundations.log_metric('Accuracy', subtraction_result)

cached_subtraction_result = subtract(44,2)
foundations.log_metric('Cached_accuracy', cached_subtraction_result)