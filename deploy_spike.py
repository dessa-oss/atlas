from vcat import *

def print_it(self):
  print(self)

pipe = pipeline | 'wonderful' | print_it
job_123 = Job(pipe)

with open('job.bin', 'w+b') as file:
  file.write(job_123.serialize())