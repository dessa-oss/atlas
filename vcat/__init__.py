# UGLY (DEVS)
class Stage(object):

  def __init__(self, uuid, function, metadata_function, *args, **kwargs):
    self.uuid = uuid
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self._metadata_function = metadata_function
  
  def run(self, *local_args):
    return self.function(*(local_args + self.args), **self.kwargs)
  
  def name(self):
    return str(self.uuid)

  def function_name(self):
    return self._metadata_function.__name__
  
class StageConnector(object):
  def __init__(self, current_stage, previous_connectors):
    self._current_stage = current_stage
    self._previous_connectors = previous_connectors
    self._has_run = False
    self._result = None
  
  def name(self):
    return self._current_stage.name()

  def function_name(self):
    return self._current_stage.function_name()

  def args(self):
    return self._current_stage.args

  def kwargs(self):
    return self._current_stage.kwargs

  def tree_names(self):
    parent_trees = [connector.tree_names() for connector in self._previous_connectors]
    return {"stage": self.name(), "function_name": self.function_name(), "args": self.args(), "kwargs": self.kwargs(), "parents": parent_trees}
      
  def stage(self, next_stage):
    return StageConnector(next_stage, [self])
  
  def run(self, *args, **kwargs):
    if self._has_run:
      return self._result
    else:
      previous_results = [connector.run() for connector in self._previous_connectors]
      list_args = list(args)
      self._result = self._current_stage.run(*(previous_results + list_args), **kwargs)
      self._has_run = True
      return self._result

  def serialize(self):
    import dill as pickle
    return pickle.dumps(self)
  
  @staticmethod
  def deserialize(serialized_self):
    import dill as pickle
    return pickle.loads(serialized_self)


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
      return self._pipe.stage(stage_args)
    
    
# PRETTY (ERIC)
class StageConnectorWrapper(object):
  def __init__(self, connector, pipeline_context, stage_context):
    self._connector = connector
    self._stage_context = stage_context
    self._stage_piping = StagePiping(self)
    self._pipeline_context = pipeline_context

  def tree_names(self):
    return self._connector.tree_names()
        
  def stage(self, function, *args, **kwargs):
    return StageConnectorWrapper(self._connector.stage(self._stage_context.make_stage(function, *args, **kwargs)), self._pipeline_context, self._stage_context)
  
  def __or__(self, stage_args):
    return self._stage_piping.pipe(stage_args)

  # TODO: make _current_stage public
  def run(self, *args, **kwargs):
    self._pipeline_context.provenance[self._connector._current_stage.uuid] = self._connector.tree_names() 
    return self._connector.run(*args, **kwargs)
  
  def __call__(self, *args, **kwargs):
    return self.run(*args, **kwargs)

  def serialize(self):
    return self._connector.serialize()
  
  @staticmethod
  def deserialize(serialized_self, pipeline_context, stage_context):
    return StageConnectorWrapper(StageConnector.deserialize(serialized_self), pipeline_context, stage_context)
  
  def splice(self, num_children):
    def splice_at(data_frames, slot_num):
      return data_frames[slot_num]

    children = []

    for i in range(num_children):
      child = self | (splice_at, i)
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

# PRETTY (BUT NOT ERIC)
class PipelineContext(object):

  def __init__(self):
    import uuid

    self.results = {}
    self.predictions = {}
    self.provenance = {}
    self.meta_data = {}
    self.file_name = str(uuid.uuid4()) + ".json"

  def save(self, result_saver):
    result_saver.save(self.file_name, {'results': self.results, 'provenance': self.provenance, "meta_data": self.meta_data})

class RedisResultSaver(object):
  def __init__(self):
    import redis

    self._connection = redis.Redis()

  def save(self, name, results):
    import pickle

    results_serialized = pickle.dumps(results)
    self._connection.sadd("result_names", name)
    self._connection.set("results:" + name, results_serialized)

class ResultReader(object):
  
  def __init__(self):
    # import glob
    # import json

    # self.results = []
    # file_list = glob.glob('*.json')
    # for file_name in file_list:
    #   with open(file_name) as file:
    #     self.results.append(json.load(file))

    self.results = RedisFetcher().fetch_results()
  
  def to_pandas(self):
    import pandas
    return pandas.DataFrame(self.results)

  def as_json(self):
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


pipeline_context = PipelineContext()
pipeline = Pipeline(pipeline_context)