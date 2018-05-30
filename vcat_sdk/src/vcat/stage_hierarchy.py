class StageHierarchy(object):

  def __init__(self):
    self.entries = {}
  
  def add_entry(self, uuid, function_name, parents, function_source_code, source_file, source_line, stage_args):
    entry = StageHierarchyEntry(uuid, function_name, parents, function_source_code, source_file, source_line, stage_args)
    self.entries[uuid] = entry

    
class StageHierarchyEntry(object):

  def __init__(self, uuid, function_name, parents, function_source_code, source_file, source_line, stage_args):
    self.parents = parents
    self.function_name = function_name
    self.uuid = uuid
    self.cache_uuid = "fake0-00000-00000-00000-00000"
    self.function_source_code = function_source_code
    self.source_file = source_file
    self.source_line = source_line
    self.stage_args = stage_args
    # self.kwargs = {}