import foundations
from model import incr_by_10, mult

incr_by_10 = foundations.create_stage(incr_by_10)
mult = foundations.create_stage(mult)

foundations.set_project_name("demo_project")

# input to model
x = 20

# build step1 of model
incr_value = incr_by_10(x)
incr_value.enable_caching()

# build step2 of model
result = mult(x, incr_value)

# run the model
result.run()
