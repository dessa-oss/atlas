from vcat import Job, LocalFileSystemResultSaver

import glob
import yaml
import time
import sys

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
  
  global_provenance = {}
  pipeline_context.provenance["global"] = global_provenance

  pipeline_context.start_time = time.time()
  try:
    job.run()
  except Exception as error:
    exception_info = sys.exc_info()
    pipeline_context.add_pipeline_error(exception_info)
  pipeline_context.end_time = time.time()
  pipeline_context.delta_time = pipeline_context.end_time - pipeline_context.start_time

  global_provenance["python_version"] = {
    "major": sys.version_info.major,
    "minor": sys.version_info.minor,
    "micro": sys.version_info.micro,
    "releaselevel": sys.version_info.releaselevel,
    "serial": sys.version_info.serial,
  }

  pipeline_context.save(LocalFileSystemResultSaver())
  if "result_savers" in pipeline_context.config:
    for result_saver_type in pipeline_context.config["result_savers"]:
      pipeline_context.save(result_saver_type())

  if pipeline_context.pipeline_error is not None:
    raise exception_info[0], exception_info[1], exception_info[2]

if __name__ == "__main__":
  main()