class PipelineContext(object):

  def __init__(self):
    import uuid

    self.results = {}
    self.predictions = {}
    self.file_name = str(uuid.uuid4()) + ".json"

  def stage(self, stage_function, *args, **kwargs):
    return stage_function(self, *args, **kwargs)

  def save(self):
    import json

    with open(self.file_name, "w+") as file:
        json.dump(self.results, file)

class ResultReader(object):
  
  def __init__(self):
    import glob
    import json

    self.results = []
    file_list = glob.glob('*.json')
    for file_name in file_list:
      with open(file_name) as file:
        self.results.append(json.load(file))
  
  def to_pandas(self):
    import pandas
    return pandas.DataFrame(self.results)

pipeline_context = PipelineContext()