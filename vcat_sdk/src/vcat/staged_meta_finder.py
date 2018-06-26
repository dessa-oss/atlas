from importlib.abc import MetaPathFinder


class StagedMetaFinder(MetaPathFinder):
    STAGED_PREFIX = 'staged_'

    def find_spec(self, fullname, path, target=None):
      from vcat.staged_module_loader import StagedModuleLoader
      from importlib import import_module
      from importlib.util import spec_from_file_location

      if fullname.startswith(StagedMetaFinder.STAGED_PREFIX):
            module_name = fullname[len(StagedMetaFinder.STAGED_PREFIX):]
            inner_module = import_module(module_name)
            return spec_from_file_location(fullname, loader=StagedModuleLoader(inner_module))

      return None
