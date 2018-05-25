from vcat import Job, LocalFileSystemResultSaver, GCPResultSaver, GCPBundledResultSaver

import glob
import yaml

def main():
  config = {}
  file_list = glob.glob('*.config.yaml')
  for file_name in file_list:
    with open(file_name, 'r') as file:
      config.update(yaml.load(file))

  job_name = config.get('job_name', 'job')
  job_binary_path = job_name + '.bin'

  with open(job_binary_path, 'rb') as file:
    job = Job.deserialize(file.read())

  pipeline_context = job._pipeline_connector._pipeline_context
  pipeline_context.config.update(config)

  try:
    job.run()
  except Exception as error:
    import sys, traceback
    exception_info = sys.exc_info()
    pipeline_context.error = {
      "type": exception_info[0],
      "exception": exception_info[1],
      "traceback": traceback.extract_tb(exception_info[2])
    }

  pipeline_context.save(LocalFileSystemResultSaver())
  pipeline_context.save(GCPResultSaver())
  pipeline_context.save(GCPBundledResultSaver())

  if pipeline_context.error is not None:
    raise exception_info[0], exception_info[1], exception_info[2]

if __name__ == "__main__":
  main()