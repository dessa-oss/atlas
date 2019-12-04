import os
os.environ['FOUNDATIONS_COMMAND_LINE'] = 'True'

import foundations
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--project-name", type=str, default=None)
parser.add_argument("--scheduler", type=str, default=None)
parser.add_argument("--job-directory", type=str, default=None)
parser.add_argument("--entrypoint", type=str, default=None)
parser.add_argument("command", nargs=argparse.REMAINDER)

args = parser.parse_args(sys.argv[1:])

foundations.submit(scheduler_config=args.scheduler,
                   job_directory=args.job_directory,
                   project_name=args.project_name,
                   entrypoint=args.entrypoint,
                   command=args.command)
