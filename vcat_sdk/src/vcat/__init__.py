# UGLY (DEVS)
class ArgumentFiller(object):
  def __init__(self, argument_fill, *args, **kwargs):
    self._argument_fill = argument_fill
    self.args = args
    self.kwargs = kwargs

  def fill(self, **kwargs):
    new_args = []
    for arg in self.args:
      self._fill_arg(new_args, arg, kwargs)
      
    new_kwargs = {}
    for keyword, arg in self.kwargs.items():
      self._fill_kwarg(new_kwargs, keyword, arg, kwargs)

    return new_args, new_kwargs

  def _fill_arg(self, new_args, arg, kwargs):
    if not self._argument_fill.fill_arg_template(new_args, arg, kwargs):
      new_args.append(arg)

  def _fill_kwarg(self, new_kwargs, keyword, arg, kwargs):
    if not self._argument_fill.fill_kwarg_template(new_kwargs, keyword, arg, kwargs):
      new_kwargs[keyword] = arg

class SuccessiveArgumentFiller(object):
  def __init__(self, fill_types, *args, **kwargs):
    self.fills = [fill_type() for fill_type in fill_types]
    self.start_args = args
    self.start_kwargs = kwargs

  def fill(self, **fill_kwargs):
    args = self.start_args
    kwargs = self.start_kwargs
    for fill in self.fills:
      filler = ArgumentFiller(fill, *args, **kwargs)
      args, kwargs = filler.fill(**fill_kwargs)
    return args, kwargs

class Stage(object):

  def __init__(self, uuid, function, metadata_function, *args, **kwargs):
    self.uuid = uuid
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self._metadata_function = metadata_function
  
  def run(self, previous_results, filler_builder, **filler_kwargs):
    filler = filler_builder(*self.args, **self.kwargs)
    new_args, new_kwargs = filler.fill(**filler_kwargs)
    return self.function(*(previous_results + new_args), **new_kwargs)
  
  def name(self):
    return str(self.uuid)

  def function_name(self):
    return self._metadata_function.__name__
  
class StageConnector(object):
  def __init__(self, current_stage, previous_connectors):
    self.current_stage = current_stage
    self._previous_connectors = previous_connectors
    self._has_run = False
    self._result = None
  
  def _reset_state(self):
    self._has_run = False
    self._result = None

    for previous_connector in self._previous_connectors:
      previous_connector._reset_state()

  def name(self):
    return self.current_stage.name()

  def function_name(self):
    return self.current_stage.function_name()

  def args(self):
    return self.current_stage.args

  def kwargs(self):
    return self.current_stage.kwargs

  def add_tree_names(self, stages_dict, filler_builder, **filler_kwargs):
    parent_ids = [connector.add_tree_names(stages_dict, filler_builder, **filler_kwargs) for connector in self._previous_connectors]
    filler = filler_builder(*self.args(), **self.kwargs())
    args, kwargs = filler.fill(**filler_kwargs)
    this_stage = {"function_name": self.function_name(), "args": args, "kwargs": kwargs, "parents": parent_ids}
    stages_dict[self.name()] = this_stage
    return self.name()
      
  def stage(self, next_stage):
    return StageConnector(next_stage, [self])
  
  def run(self, filler_builder, **filler_kwargs):
    if self._has_run:
      return self._result
    else:
      previous_results = [connector.run(filler_builder, **filler_kwargs) for connector in self._previous_connectors]
      self._result = self.current_stage.run(previous_results, filler_builder, **filler_kwargs)
      self._has_run = True
      return self._result

class StageGraph(object):
  def stage(self, stage):
    return StageConnector(stage, [])
  
  def join(self, stage, upstream_connectors):
    return StageConnector(stage, upstream_connectors)

class StageContext(object):
  def __init__(self, pipeline_context):
    self._pipeline_context = pipeline_context

  def make_stage(self, function, *args, **kwargs):
    import uuid
    stage_uuid = uuid.uuid4()
    stage_uuid = str(stage_uuid)
    return Stage(stage_uuid, self._wrapped_function(stage_uuid, function), function, *args, **kwargs)

  def _wrapped_function(self, stage_uuid, function):
    def wrapped(*args, **kwargs):
      import time

      start_time = time.time()
      stage_output = function(*args, **kwargs)
      end_time = time.time()
      if isinstance(stage_output, tuple):
        return_value, result = stage_output
        self._pipeline_context.results[stage_uuid] = result
      else:
        return_value = stage_output
      self._pipeline_context.meta_data[stage_uuid] = {
        "start_time": start_time,
        "end_time": end_time,
        "delta_time": end_time - start_time,
      }
      return return_value
    return wrapped

class StagePiping(object):
  def __init__(self, pipe):
      self._pipe = pipe

  def pipe(self, stage_args):
    if isinstance(stage_args, tuple):
      function = stage_args[0]
      args = list(stage_args[1:])
      last_argument = args[-1]
      if isinstance(last_argument, dict):
        kwargs = last_argument
        args.pop()
        return self._pipe.stage(function, *args, **kwargs)
      else:
        return self._pipe.stage(function, *args)
    else:
      if callable(stage_args):
        function = stage_args
      else:
        def constant():
          return stage_args
        function = constant
      
      return self._pipe.stage(function)

class JobBundler(object):
  def __init__(self, job_name, config, job):
    import os

    self._config = config
    self._config['job_name'] = job_name

    self._job_name = job_name
    self._job = job
    self._module_directory = os.path.dirname(os.path.abspath(__file__))
    self._resource_directory = self._module_directory + "/resources"

  def job_name(self):
    return self._job_name

  def bundle(self):
    self._save_job()
    self._save_config()
    self._bundle_job()

  def cleanup(self):
    import os
    os.remove(self.job_archive())
    os.remove(self._job_binary())
    os.remove(self._job_config_yaml())

  def job_archive_name(self):
    return self._job_name + ".tgz"

  def job_archive(self):
    return "../" + self.job_archive_name()
  
  def _job_binary(self):
    return self._job_name + ".bin"

  def _job_results_archive(self):
    return self._job_name + ".results.tgz"
  
  def _job_config_yaml(self):
    return self._job_name + ".config.yaml"

  def _save_job(self):
    with open(self._job_binary(), "w+b") as file:
      file.write(self._job.serialize())

  def _save_config(self):
    import yaml
    with open(self._job_config_yaml(), 'w+') as file:
      yaml.dump(self._config, file)

  def _bundle_job(self):
    import tarfile
    import glob
    import os

    current_directory = os.getcwd()
    # os.chdir(self._module_directory)

    with tarfile.open(self.job_archive(), "w:gz") as tar:
      tar.add(".", arcname=self._job_name)

      os.chdir(self._module_directory)
      tar.add(".", arcname=self._job_name + "/vcat")

      os.chdir(self._resource_directory)
      tar.add(".", arcname=self._job_name)

    os.chdir(current_directory)

# PRETTY (BUT NOT ERIC)
class HyperparameterArgumentFill(object):
  def fill_arg_template(self, new_args, arg, kwargs):
    if isinstance(arg, Hyperparameter):
      if arg.name in kwargs:
        new_args.append(kwargs[arg.name])
      return True
    return False
    
  def fill_kwarg_template(self, new_kwargs, keyword, arg, kwargs):
    if isinstance(arg, Hyperparameter):
      if keyword in kwargs:
        new_kwargs[keyword] = kwargs[keyword]
      return True
    return False

class StageConnectorWrapperFill(object):
  def fill_arg_template(self, new_args, arg, kwargs):
    if isinstance(arg, StageConnectorWrapper):
      new_args.append(arg.run(**kwargs))
      return True
    return False
    
  def fill_kwarg_template(self, new_kwargs, keyword, arg, kwargs):
    if isinstance(arg, StageConnectorWrapper):
      new_kwargs[keyword] = arg.run(**kwargs)
      return True
    return False

class HyperparameterArgumentNameFill(object):
  def fill_arg_template(self, new_args, arg, kwargs):
    if isinstance(arg, Hyperparameter):
      arg_display = kwargs.get(arg.name, "<using default>")
      new_args.append({"hyperparameter_value": arg_display, "hyperparameter_name": arg.name})
      return True
    return False
    
  def fill_kwarg_template(self, new_kwargs, keyword, arg, kwargs):
    if isinstance(arg, Hyperparameter):
      kwarg_display = kwargs.get(keyword, "<using default>")
      new_kwargs[keyword] = {"hyperparameter_value": kwarg_display, "hyperparameter_name": keyword}
      return True
    return False

class StageConnectorWrapperNameFill(object):
  def fill_arg_template(self, new_args, arg, kwargs):
    if isinstance(arg, StageConnectorWrapper):
      new_args.append({"stage_id": arg._connector.name()})
      return True
    return False
    
  def fill_kwarg_template(self, new_kwargs, keyword, arg, kwargs):
    if isinstance(arg, StageConnectorWrapper):
      new_kwargs[keyword] = {"stage_id": arg._connector.name()}
      return True
    return False

class Job(object):
  def __init__(self, pipeline_connector, **kwargs):
    self.kwargs = kwargs
    self._pipeline_connector = pipeline_connector
  
  def run(self):
    return self._pipeline_connector.run(**self.kwargs)
  
  def serialize(self):
    import dill as pickle
    return pickle.dumps(self)
  
  @staticmethod
  def deserialize(serialized_self):
    import dill as pickle
    return pickle.loads(serialized_self)


# PRETTY (ERIC)
class Hyperparameter(object):
  def __init__(self, name=None):
    self.name = name

def grid_param_set_generator(dict_of_hyper_params):
  import itertools

  param_keys = []
  param_vals_to_select = []

  for key, val in dict_of_hyper_params.iteritems():
    param_keys.append(key)
    param_vals_to_select.append(val)

  for param_vals in itertools.product(*param_vals_to_select):
    param_set_entry = {}

    for param_key, param_val in zip(param_keys, param_vals):
      param_set_entry[param_key] = param_val

    yield param_set_entry

class StageConnectorWrapper(object):
  def __init__(self, connector, pipeline_context, stage_context):
    self._connector = connector
    self._stage_context = stage_context
    self._stage_piping = StagePiping(self)
    self._pipeline_context = pipeline_context
    self._persist = False

  def _reset_state(self):
    self._connector._reset_state()

  def tree_names(self, **filler_kwargs):
    all_stages = {}
    self._connector.add_tree_names(all_stages, self._provenance_filler_builder, **filler_kwargs)
    return all_stages
        
  def stage(self, function, *args, **kwargs):
    return StageConnectorWrapper(self._connector.stage(self._stage_context.make_stage(function, *args, **kwargs)), self._pipeline_context, self._stage_context)

  def persist(self):
    self._persist = True
  
  def __or__(self, stage_args):
    return self._stage_piping.pipe(stage_args)

  def run(self, **filler_kwargs):
    self._pipeline_context.provenance[self._connector.current_stage.uuid] = self.tree_names(**filler_kwargs)
    return self.run_without_provenance(**filler_kwargs)

  def run_without_provenance(self, **filler_kwargs):
    try:
      result = self._connector.run(self._filler_builder, **filler_kwargs)
    except:
      import sys
      self._pipeline_context.pipeline_errors[self._connector.name()] = self._pipeline_context.nice_error(sys.exc_info())
      raise
    self._pipeline_context.persisted_data[self._connector.name()] = result
    return result

  def grid_search(self, deployer_type, **hype_kwargs):
    import time
    import uuid

    hype_dict = {}

    for key, val in hype_kwargs.iteritems():
      if isinstance(val, list):
        hype_dict[key] = val
      else:
        hype_dict[key] = [val]

    for param_set in grid_param_set_generator(hype_dict):
      self._reset_state()
      job = Job(self, **param_set)
      deployer = deployer_type(str(uuid.uuid4()), job)

      deployer.deploy()

      while not deployer.is_job_complete():
        print "Waiting for job \"" + deployer.job_name() + "\" to finish..."
        time.sleep(5)

      print "Fetching results..."
      # results_dict = deployer.fetch_job_results()

      print "Job \"" + deployer.job_name() + "\" has completed."

  def adaptive_search(self, deployer_type, initial_generator, generator_function):
    def extract_results(results_dict):
      results = {}
    
      for result_entry in results_dict["results"].values():
          results.update(result_entry)
          
      return results

    import Queue
    import time
    import uuid

    queue = Queue.Queue()

    for initial_params in initial_generator:
      queue.put(initial_params)
    
    while not queue.empty():
      self._reset_state()

      param_set = queue.get()
      job = Job(self, **param_set)
      deployer = deployer_type(str(uuid.uuid4()), job)
      deployer.deploy()

      while not deployer.is_job_complete():
        print "Waiting for job \"" + deployer.job_name() + "\" to finish..."
        time.sleep(5)

      print "Fetching results..."
      results_dict = deployer.fetch_job_results()

      print "Job \"" + deployer.job_name() + "\" has completed."

      for new_params in generator_function(extract_results(results_dict)):
        queue.put(new_params)

  def _filler_builder(self, *args, **kwargs):
    return SuccessiveArgumentFiller([HyperparameterArgumentFill, StageConnectorWrapperFill], *args, **kwargs)

  def _provenance_filler_builder(self, *args, **kwargs):
    return SuccessiveArgumentFiller([HyperparameterArgumentNameFill, StageConnectorWrapperNameFill], *args, **kwargs)
  
  def __call__(self, *args, **kwargs):
    return self.run(*args, **kwargs)

  def serialize(self):
    return self._connector.serialize()

  def name(self):
    return self._connector.name()
  
  @staticmethod
  def deserialize(serialized_self, pipeline_context, stage_context):
    return StageConnectorWrapper(StageConnector.deserialize(serialized_self), pipeline_context, stage_context)
  
  def splice(self, num_children):
    def splice_at(data_frames, slot_num):
      return data_frames[slot_num]

    children = []

    for child_index in range(num_children):
      child = self | (splice_at, child_index)
      children.append(child)

    return children

class Pipeline(object):
  def __init__(self, pipeline_context):
    self.graph = StageGraph()
    self.pipeline_context = pipeline_context
    self._stage_context = StageContext(self.pipeline_context)
    self._stage_piping = StagePiping(self)
      
  def stage(self, function, *args, **kwargs):
    current_stage = self._stage_context.make_stage(function, *args, **kwargs)
    return StageConnectorWrapper(self.graph.stage(current_stage), self.pipeline_context, self._stage_context)
  
  def join(self, upstream_connector_wrappers, function, *args, **kwargs):
    upstream_connectors = [wrapper._connector for wrapper in upstream_connector_wrappers]
    current_stage = self._stage_context.make_stage(function, *args, **kwargs)
    return StageConnectorWrapper(self.graph.join(current_stage, upstream_connectors), self.pipeline_context, self._stage_context)  

  def __or__(self, stage_args):
    return self._stage_piping.pipe(stage_args)

class GCPJobDeployment(object):
  def __init__(self, job_name, job):
    from google.cloud.storage import Client
    from googleapiclient import discovery

    self._config = {}

    self._gcp_bucket_connection = Client()
    self._code_bucket_connection = self._gcp_bucket_connection.get_bucket('tango-code-test')
    self._result_bucket_connection = self._gcp_bucket_connection.get_bucket('tango-result-test')

    self._job_name = job_name
    self._job = job
    self._job_bundler = JobBundler(self._job_name, self._config, self._job)
    self._job_result_object = self._result_bucket_connection.blob(self._job_archive_name())

    self._job_results = None

  def config(self):
    return self._config

  def job_name(self):
    return self._job_name

  def deploy(self):
    self._job_bundler.bundle()
    try:
      self._run()
    finally:
      self._job_bundler.cleanup()

  def is_job_complete(self):
    return self._job_result_object.exists()

  def fetch_job_results(self):
    import os
    import tarfile
    import pickle

    if self._job_results is None:
      with open(self._job_results_archive(), 'w+b') as file:
        self._job_result_object.download_to_file(file)

      result = None
      with tarfile.open(self._job_results_archive(), "r:gz") as tar:
        for tarinfo in tar:
            if os.path.splitext(tarinfo.name)[1] == ".pkl":
                file = tar.extractfile(tarinfo)
                result = pickle.load(file)
                file.close()

      self._remove_job_results_archive()
      self._job_results = result

    return self._job_results

  def _run(self):
    job_object = self._code_bucket_connection.blob(self._job_archive_name())
    with open(self._job_archive(), 'rb') as file:
      job_object.upload_from_file(file)

  def _job_archive_name(self):
    return self._job_bundler.job_archive_name()

  def _job_archive(self):
    return self._job_bundler.job_archive()

  def _job_results_archive(self):
    return self._job_name + ".results.tgz"

  def _remove_job_results_archive(self):
    import os
    os.remove(self._job_results_archive())

class LocalShellJobDeployment(object):
  def __init__(self, job_name, job):
    self._config = {}
    self._job_name = job_name
    self._job = job
    self._job_bundler = JobBundler(self._job_name, self._config, self._job)
    self._results = {}

  def config(self):
    return self._config

  def job_name(self):
    return self._job_name

  def deploy(self):
    self._job_bundler.bundle()
    try:
      self._run()
    finally:
      self._job_bundler.cleanup()

  def is_job_complete(self):
    return True

  def fetch_job_results(self):
    return self._results

  def _run(self):
    import shutil, subprocess, glob
    import dill as pickle
    script = "tar -xvf " + self._job_bundler.job_archive() + " && " + \
      "cd " + self._job_name + " && " + \
      "sh ./run.sh"
    args = ['/usr/bin/env', 'sh', '-c', script]
    subprocess.call(args)

    file_name = glob.glob(self._job_name + '/*.pkl')[0]
    with open(file_name, 'rb') as file:
      self._results = pickle.load(file)

    shutil.rmtree(self._job_name)

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

# PRETTY (BUT NOT ERIC)
class PipelineContext(object):

  def __init__(self):
    import uuid

    self.results = {}
    self.config = {}
    self.predictions = {}
    self.provenance = {}
    self.meta_data = {}
    self.persisted_data = {}
    self.error = None
    self.pipeline_errors = {}
    self.file_name = str(uuid.uuid4()) + ".json"

  def save(self, result_saver):
    result_saver.save(self.file_name, self._context())

  def nice_error(self, exception_info):
    import traceback
    return {
      "type": exception_info[0],
      "exception": exception_info[1],
      "traceback": traceback.extract_tb(exception_info[2])
    }

  def _context(self):
    return {
      "results": self.results, 
      "config": self.config, 
      "provenance": self.provenance, 
      "meta_data": self.meta_data,
      "persisted_data": self.persisted_data,
      "error": self.error,
      "pipeline_errors": self.pipeline_errors,
    }

class LocalFileSystemResultSaver(object):
  def save(self, name, results):
    import pickle

    file_name = name + ".pkl"
    with open(file_name, 'w+b') as file:
      pickle.dump(results, file)

class RedisResultSaver(object):
  def __init__(self):
    import redis

    self._connection = redis.Redis()

  def save(self, name, results):
    import dill as pickle

    results_serialized = pickle.dumps(results)
    self._connection.sadd("result_names", name)
    self._connection.set("results:" + name, results_serialized)

  def clear(self):
    return self._connection.delete("result_names")

class GCPResultSaver(object):
  def __init__(self):
    from google.cloud.storage import Client
    from googleapiclient import discovery

    self._gcp_bucket_connection = Client()
    self._result_bucket_connection = self._gcp_bucket_connection.get_bucket('tango-result-test')

  def save(self, name, results):
    import dill as pickle

    result_object = self._result_bucket_connection.blob("contexts/" + name + ".pkl")
    serialized_results = pickle.dumps(results)
    result_object.upload_from_string(serialized_results)

  def clear(self):
    pass

class GCPBundledResultSave(object):
  def __init__(self, name, results):
    from google.cloud.storage import Client
    from googleapiclient import discovery

    self._gcp_bucket_connection = Client()
    self._result_bucket_connection = self._gcp_bucket_connection.get_bucket('tango-result-test')
    self._name = name
    self._results = results
    self._persisted_results = results.pop("persisted_data", {})

    self._results["persisted_data"] = {}
    for key in self._persisted_results.keys():
      self._results["persisted_data"][key] = self._persisted_name(key)

  def save(self):
    import os

    self._serialize_context()
    self._serialize_persisted()
    self._bundle_results()

    result_object = self._result_bucket_connection.blob(self._bucketed_bundle_name())
    with open(self._bundle_name(), "rb") as file:
      result_object.upload_from_file(file)

    os.remove(self._bundle_name())
    for key in self._persisted_results:
      os.remove(self._persisted_name(key))
    os.remove(self._context_name())

  def _context_name(self):
    return "context.pkl"

  def _persisted_name(self, stage_name):
    return stage_name + ".persisted.pkl"

  def _bundle_name(self):
    return self._name + ".tgz"

  def _bucketed_bundle_name(self):
    return "bundled_contexts/" + self._bundle_name()

  def _serialize_context(self):
    import dill as pickle
    with open(self._context_name(), "w+b") as file:
      pickle.dump(self._results, file)
  
  def _bundle_results(self):
    import tarfile
    import uuid

    with tarfile.open(self._bundle_name(), "w:gz") as tar:
      for key in self._persisted_results:
        self._add_to_tar(tar, self._persisted_name(key))
      self._add_to_tar(tar, self._context_name())

  def _add_to_tar(self, tar, name):
    tar.add(name, arcname=self._name + "/" + name)

  def _serialize_persisted(self):
    import dill as pickle
    for key, value in self._persisted_results.items():
      with open(self._persisted_name(key), "w+b") as file:
        pickle.dump(value, file)

class GCPBundledResultSaver(object):
  def save(self, name, results):
    GCPBundledResultSave(name, results).save()

  def clear(self):
    pass

def restructure_headers(all_headers, first_headers):
  def diff(list_0, list_1):
    set_1 = set(list_1)
    return [item for item in list_0 if item not in set_1]

  return first_headers + diff(all_headers, first_headers)

class ResultReader(object):
  def __init__(self, result_fetcher):
    self.results = result_fetcher.fetch_results()
  
  def _to_pandas(self):
    import pandas
    return pandas.DataFrame(self.results)

  def _as_dict(self):
    return self.results

  def _as_json(self):
    import json
    return json.dumps(self.results)

  def get_job_information(self):
    import datetime
    import pandas as pd

    all_job_information = []

    main_headers = ["Job ID", "Job Status", "Stage ID", "Parent Stage IDs", "Stage Name", "Args", "Kwargs", "Start Time", "End Time", "Elapsed Time"]

    for job_result in self.results:
      job_id = job_result["config"]["job_name"]
      job_status = None

      try:
        if job_result["error"]:
          job_status = "failed"
        else:
          job_status = "succeeded"
      except:
        job_status = "succeeded"

      meta_data = job_result["meta_data"]

      for entry_key, stage_set in job_result["provenance"].iteritems():
        if entry_key != "global":
          for stage_id, stage_info in stage_set.iteritems():
            stage_name = stage_info["function_name"]
            column_headers = list(main_headers)
            
            start_time = None
            end_time = None
            elapsed_time = None

            try:
              meta_data_entry = meta_data[stage_id]

              start_time = datetime.datetime.fromtimestamp(meta_data_entry["start_time"])
              end_time = datetime.datetime.fromtimestamp(meta_data_entry["end_time"])
              elapsed_time = meta_data_entry["delta_time"]
            except:
              pass

            stage_name = stage_info.get("function_name", None)
            parent_stage_ids = stage_info["parents"]

            args = []
            kwargs = {}
            row_data = [job_id, job_status, stage_id, parent_stage_ids, stage_name, args, kwargs, start_time, end_time, elapsed_time]
            
            for arg in stage_info["args"]:
              if isinstance(arg, dict):
                try:
                  arg_stage_id = arg["stage_id"]
                  args.append(arg_stage_id)

                  parent_stage_ids.append(arg_stage_id)
                except:
                  hyperparameter_name = arg.get("hyperparameter_name", None)
                  hyperparameter_value = arg["hyperparameter_value"]

                  if hyperparameter_name:
                    args.append(hyperparameter_name)

                    column_headers.append(hyperparameter_name)
                    row_data.append(hyperparameter_value)
                  else:
                    args.append(hyperparameter_value)
              else:
                args.append(arg)

            for arg_name, arg_val in stage_info["kwargs"].iteritems():
              if isinstance(arg_val, dict):
                try:
                  arg_val_stage_id = arg_val["stage_id"]
                  kwargs.update({arg_name: arg_val_stage_id})

                  parent_stage_ids.append(arg_val_stage_id)
                except:
                  hyperparameter_name = arg_val.get("hyperparameter_name", None)
                  hyperparameter_value = arg_val["hyperparameter_value"]

                  if hyperparameter_name:
                    kwargs.update({arg_name: hyperparameter_name})

                    column_headers.append(hyperparameter_name)
                    row_data.append(hyperparameter_value)
                  else:
                    kwargs.append({arg_name: hyperparameter_value})
              else:
                kwargs.update({arg_name: arg_val})

            all_job_information.append(pd.DataFrame(data=[row_data], columns=column_headers))

    output_dataframe = pd.concat(all_job_information, ignore_index=True)
    fixed_headers = restructure_headers(list(output_dataframe), main_headers)
    return output_dataframe[fixed_headers]

  def get_results(self):
    import pandas as pd

    all_job_information = []
    main_headers = ["Job ID", "Stage ID", "Stage Name", "Has Unstructured Result?"]

    for job_result in self.results:
      job_id = job_result["config"]["job_name"]
      persisted_data = job_result["persisted_data"]

      structured_results = job_result["results"]
      stage_ids_with_names = {}

      for entry_key, stage_set in job_result["provenance"].iteritems():
        if entry_key != "global":
          for stage_id, stage_info in stage_set.iteritems():
            stage_name = stage_info["function_name"]
            stage_ids_with_names.update({stage_id: stage_name})

      for stage_id, stage_name in stage_ids_with_names.iteritems():
        column_headers = list(main_headers)
        has_unstructured_result = None

        try:
          has_unstructured_result = persisted_data[stage_id] is not None
        except:
          has_unstructured_result = False

        row_data = [job_id, stage_id, stage_name, has_unstructured_result]

        try:
          for structured_result_name, structured_result_val in structured_results[stage_id].iteritems():
            column_headers.append(structured_result_name)
            row_data.append(structured_result_val)
        except:
          pass

        all_job_information.append(pd.DataFrame(data=[row_data], columns=column_headers))

    output_dataframe = pd.concat(all_job_information, ignore_index=True)
    fixed_headers = restructure_headers(list(output_dataframe), main_headers)
    return output_dataframe[fixed_headers]

  def get_unstructured_results(self, stage_ids):
    def get_unstructured_result(stage_id):
      result = None

      for job_result in self.results:
        persisted_data = job_result["persisted_data"]
        try:
          result = persisted_data[stage_id]
        except:
          continue

      return result

    return map(get_unstructured_result, stage_ids)

class LocalFileSystemFetcher(object):
  def fetch_results(self):
    import glob
    import pickle

    self.results = []
    file_list = glob.glob('*.pkl')
    for file_name in file_list:
      with open(file_name, 'rb') as file:
        self.results.append(pickle.load(file))
    return self.results

class RedisFetcher(object):
  def __init__(self):
    import redis

    self._connection = redis.Redis()

  def fetch_results(self):
    import pickle

    result_names = self._connection.smembers("result_names")
    result_keys = ["results:" + name.decode("utf-8") for name in result_names]
    results_serialized = [self._connection.get(key) for key in result_keys]
    return [pickle.loads(result_serialized) for result_serialized in results_serialized]

class GCPFetcher(object):
  def __init__(self):
    from google.cloud.storage import Client
    from googleapiclient import discovery

    self._gcp_bucket_connection = Client()
    self._result_bucket_connection = self._gcp_bucket_connection.get_bucket('tango-result-test')

  def fetch_results(self):
    import dill as pickle

    objects = self._result_bucket_connection.list_blobs(prefix="contexts/")
    results_serialized = [result_object.download_as_string() for result_object in objects]
    return [pickle.loads(result_serialized) for result_serialized in results_serialized]

class GCPBundleFetcher(object):
  def __init__(self):
    from google.cloud.storage import Client
    from googleapiclient import discovery

    self._gcp_bucket_connection = Client()
    self._result_bucket_connection = self._gcp_bucket_connection.get_bucket('tango-result-test')

  def fetch_results(self):
    import os
    import dill as pickle
    import tarfile
    import shutil

    objects = self._result_bucket_connection.list_blobs(prefix="bundled_contexts/")
    results = []
    for result_object in objects:
      file_name = os.path.basename(result_object.name)
      with open(file_name, "w+b") as file:
        result_object.download_to_file(file)
      directory_name = os.path.splitext(file_name)[0]
      with tarfile.open(file_name, "r:gz") as tar:
        tar.extractall()
      with open(directory_name + "/context.pkl", "rb") as file:
        context = pickle.load(file)

      persisted_data = context["persisted_data"]
      for key, value in persisted_data.items():
        with open(directory_name + "/" + value, "rb") as file:
          persisted_data[key] = pickle.load(file)
      results.append(context)

      shutil.rmtree(directory_name)
      os.remove(file_name)
    return results

pipeline_context = PipelineContext()
pipeline = Pipeline(pipeline_context)