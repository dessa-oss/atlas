import os
os.environ['FOUNDATIONS_COMMAND_LINE'] = 'True'

import foundations
import sys

foundations.submit(scheduler_config="scheduler", job_directory=sys.argv[1], command=["main.py", sys.argv[2], sys.argv[3], sys.argv[4]])
