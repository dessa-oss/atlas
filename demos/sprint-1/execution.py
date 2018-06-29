from vcat import * # required for below to work
from staged_methods import *

# create a stage from the create_data_frame method
data = create_data_frame()
 
# create a stage from the print_it metho
log = print_it(data)
 
# execute the stage
job = log.run()

# we can print the status of the job
print("Job Status: {}".format(job.get_job_status()))

# we can wait for the job to complete
job.wait_for_deployment_to_complete()
