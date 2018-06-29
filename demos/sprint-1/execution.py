from vcat import * # required for below to work
from staged_methods import *

# create a stage from the create_data_frame method
data = create_data_frame()
 
# create a stage from the print_it metho
log = print_it(data)
 
# execute the stage
log.run()