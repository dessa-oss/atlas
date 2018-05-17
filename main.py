from vcat import Job, LocalFileSystemResultSaver

with open('job.bin', 'rb') as file:
  job = Job.deserialize(file.read())
  job.run()
  job._pipeline_connector._pipeline_context.save(LocalFileSystemResultSaver())

