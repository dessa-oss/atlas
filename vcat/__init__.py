class PipelineExecutor(object):
  def __init__(self, pipeline_context):
    self.pipeline_context = pipeline_context

  def execute(self, stage_function, *args, **kwargs):
    self.pipeline_context.results.update(kwargs)
    return stage_function(self.pipeline_context, *args, **kwargs)

class PipelineContext(object):

  def __init__(self):
    import uuid

    self.results = {}
    self.predictions = {}
    self.file_name = str(uuid.uuid4()) + ".json"

  def simple_stage(self, stage_function, *args, **kwargs):
    return PipelineExecutor(self).execute(stage_function, *args, **kwargs)

  def stage(self, stage_function, *args, **kwargs):
    def executor_function(pipeline_context, *args, **kwargs):
      stage_output = stage_function(*args, **kwargs)
      if isinstance(stage_output, tuple):
        return_value, result = stage_output
        self.results.update(result)
      else:
        return_value = stage_output
      return return_value

    return PipelineExecutor(self).execute(executor_function, *args, **kwargs)

  def save(self, result_saver):
    result_saver.save(self.file_name, self.results)

class RedisResultSaver(object):
  def __init__(self):
    import redis

    self._connection = redis.Redis()

  def save(self, name, results):
    import json

    results_serialized = json.dumps(results)
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

class RedisFetcher(object):
  def __init__(self):
    import redis

    self._connection = redis.Redis()

  def fetch_results(self):
    import json

    result_names = self._connection.smembers("result_names")
    result_keys = ["results:" + name.decode("utf-8") for name in result_names]
    results_serialized = [self._connection.get(key) for key in result_keys]
    return [json.loads(result_serialized) for result_serialized in results_serialized]

pipeline_context = PipelineContext()