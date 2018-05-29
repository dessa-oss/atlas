from gcp_bundle_fetcher import GCPBundleFetcher
from gcp_bundled_result_saver import GCPBundledResultSaver
from gcp_fetcher import GCPFetcher
from gcp_job_deployment import GCPJobDeployment
from gcp_result_saver import GCPResultSaver
from hyperparameter import Hyperparameter
from job import Job
from local_file_system_fetcher import LocalFileSystemFetcher
from local_file_system_result_saver import LocalFileSystemResultSaver
from local_shell_job_deployment import LocalShellJobDeployment
from pipeline_context import PipelineContext
from pipeline import Pipeline
from redis_fetcher import RedisFetcher
from redis_result_saver import RedisResultSaver
from result_reader import ResultReader
from stage_context import StageContext

def gcp_deploy_job(job, job_name):
  deployment = GCPJobDeployment(job_name, job)
  deployment.deploy()
  return deployment

def wait_for_deployment_to_complete(deployment):
  import time

  while not deployment.is_job_complete():
    print("waiting for job `" + deployment.job_name() + "` to finish")
    time.sleep(6)
  
  print("job `" + deployment.job_name() + "`completed")

def raise_error_if_job_failed(deployment):
  if deployment.is_job_complete():
    results = deployment.fetch_job_results()
    if results and results["error"]:
      raise results["error"]["type"], results["error"]["exception"], None

def restructure_headers(all_headers, first_headers):
  def diff(list_0, list_1):
    set_1 = set(list_1)
    return [item for item in list_0 if item not in set_1]

  return first_headers + diff(all_headers, first_headers)

pipeline_context = PipelineContext()
pipeline = Pipeline(pipeline_context)