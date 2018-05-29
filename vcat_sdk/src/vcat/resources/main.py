from vcat import Job, LocalFileSystemResultSaver, JobSourceBundle

import glob
import yaml
import time
import sys

def main():
  job_source_bundle = JobSourceBundle('job', './')

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
  global_stage_context = pipeline_context.global_stage_context
  pipeline_context.provenance.config.update(config)
  config = pipeline_context.provenance.config

  pipeline_context.provenance.job_source_bundle = job_source_bundle
  
  global_provenance = {}
  pipeline_context.provenance.stage_provenance["global"] = global_provenance

  global_stage_context.start_time = time.time()
  try:
    job.run()
  except Exception as error:
    exception_info = sys.exc_info()
    global_stage_context.add_error_information(exception_info)
  global_stage_context.end_time = time.time()
  global_stage_context.delta_time = global_stage_context.end_time - global_stage_context.start_time

  global_provenance["python_version"] = {
    "major": sys.version_info.major,
    "minor": sys.version_info.minor,
    "micro": sys.version_info.micro,
    "releaselevel": sys.version_info.releaselevel,
    "serial": sys.version_info.serial,
  }

  pipeline_context.save(LocalFileSystemResultSaver())
  if "result_savers" in config:
    for result_saver_type in config["result_savers"]:
      pipeline_context.save(result_saver_type())

  if global_stage_context.error_information is not None:
    raise exception_info[0], exception_info[1], exception_info[2]

if __name__ == "__main__":
  main()