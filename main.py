from vcat import Job

with open('job.bin', 'rb') as file:
  Job.deserialize(file.read()).run()