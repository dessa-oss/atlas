from vcat import Job, LocalFileSystemResultSaver, GCPResultSaver

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
    job.run()

    pipeline_context = job._pipeline_connector._pipeline_context
    pipeline_context.config.update(config)
    pipeline_context.save(LocalFileSystemResultSaver())
    pipeline_context.save(GCPResultSaver())

if __name__ == "__main__":
  main()