plain_value = "plain_value"
hyperparameter_value = "hyperparameter_value"
stage_value = "stage_value"

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
      new_args.append({hyperparameter_value: arg_display})
      return True
    return False
    
  def fill_kwarg_template(self, new_kwargs, keyword, arg, kwargs):
    if isinstance(arg, Hyperparameter):
      kwarg_display = kwargs.get(keyword, "<using default>")
      new_kwargs[keyword] = {hyperparameter_value: kwarg_display}
      return True
    return False

class StageConnectorWrapperNameFill(object):
  def fill_arg_template(self, new_args, arg, kwargs):
    if isinstance(arg, StageConnectorWrapper):
      new_args.append({stage_value: arg._connector.name()})
      return True
    return False
    
  def fill_kwarg_template(self, new_kwargs, keyword, arg, kwargs):
    if isinstance(arg, StageConnectorWrapper):
      new_kwargs[keyword] = {stage_value: arg._connector.name()}
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
    result = self._connector.run(self._filler_builder, **filler_kwargs)
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

    self.config = {'job_name': job_name}

    self._gcp_bucket_connection = Client()
    self._code_bucket_connection = self._gcp_bucket_connection.get_bucket('tango-code-test')
    self._result_bucket_connection = self._gcp_bucket_connection.get_bucket('tango-result-test')

    self._job_name = job_name
    self._job = job
    self._job_result_object = self._result_bucket_connection.blob(self._job_archive())

  def job_name(self):
    return self._job_name

  def deploy(self):
    self._save_job()
    self._save_config()

    self._bundle_job()

    job_object = self._code_bucket_connection.blob(self._job_archive())
    with open(self._job_archive(), 'rb') as file:
      job_object.upload_from_file(file)

    self._remove_job_archive()
    self._remove_job_binary()
    self._remove_config()

  def is_job_complete(self):
    return self._job_result_object.exists()

  def fetch_job_results(self):
    import os
    import tarfile
    import pickle

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

    return result

  def _job_archive(self):
    return self._job_name + ".tgz"
  
  def _job_binary(self):
    return self._job_name + ".bin"

  def _job_results_archive(self):
    return self._job_name + ".results.tgz"
  
  def _job_config_yaml(self):
    return self._job_name + ".config.yaml"

  def _remove_job_archive(self):
    import os
    os.remove(self._job_archive())

  def _remove_job_binary(self):
    import os
    os.remove(self._job_binary())

  def _remove_job_results_archive(self):
    import os
    os.remove(self._job_results_archive())

  def _remove_config(self):
    import os
    os.remove(self._job_config_yaml())

  def _save_job(self):
    with open(self._job_binary(), "w+b") as file:
      file.write(self._job.serialize())

  def _save_config(self):
    import yaml
    with open(self._job_config_yaml(), 'w+') as file:
      yaml.dump(self.config, file)

  def _bundle_job(self):
    import tarfile

    with tarfile.open(self._job_archive(), "w:gz") as tar:
      for name in [self._job_binary(), self._job_config_yaml(), "run.sh", "main.py", "requirements.txt", "vcat"]:
          tar.add(name, arcname=self._job_name + "/" + name)

def gcp_deploy_job(job, job_name):
  deployment = GCPJobDeployment(job_name, job)
  deployment.deploy()
  return deployment

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
    self.file_name = str(uuid.uuid4()) + ".json"

  def save(self, result_saver):
    result_saver.save(self.file_name, self._context())

  def _context(self):
    return {
      "results": self.results, 
      "config": self.config, 
      "provenance": self.provenance, 
      "meta_data": self.meta_data,
      "persisted_data": self.persisted_data,
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

class ResultReader(object):
  
  def __init__(self, result_fetcher):
    self.results = result_fetcher.fetch_results()
  
  def to_pandas(self):
    import pandas
    return pandas.DataFrame(self.results)

  def as_dict(self):
    return self.results

  def as_json(self):
    import json
    return json.dumps(self.results)

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