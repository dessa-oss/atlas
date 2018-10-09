from foundations import *
from staged_model import incr_by_10, mult

foundations.set_project_name('buck')

# input to model
x = 20

# build step1 of model
incr_value = incr_by_10(x)

# build step2 of model
result = mult(x, incr_value)

# run the model
result.run()
