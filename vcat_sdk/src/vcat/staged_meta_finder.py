from importlib.abc import MetaPathFinder


class StagedMetaFinder(MetaPathFinder):
    """Used to create define specs for loading staged modules in importing modules
    """

    STAGED_PREFIX = 'staged_'
    STAGED_PREFIX_LENGTH = len(STAGED_PREFIX)

    def find_spec(self, fullname, path, target=None):
        """Find a module spec for loading

        Arguments:
          fullname {str} -- Name of the module
          path {str} -- Unused

        Keyword Arguments:
          target {str} -- Unused (default: {None})

        Returns:
          importlib._bootstrap.ModuleSpec -- ModuleSpec containing information required to import the module
        """

        if self._is_staged_module(fullname):
            return self._load_spec(fullname)

        return None

    def _load_spec(self, staged_name):
        from vcat.staged_module_loader import StagedModuleLoader
        from importlib.util import spec_from_file_location

        inner_module = self._find_module(staged_name)
        return spec_from_file_location(staged_name, loader=StagedModuleLoader(inner_module))

    def _find_module(self, staged_named):
        from importlib import import_module

        module_name = self._module_without_staged_prefix(staged_named)
        return import_module(module_name)

    def _module_without_staged_prefix(self, fullname):
        return fullname[StagedMetaFinder.STAGED_PREFIX_LENGTH:]

    def _is_staged_module(self, fullname):
        return fullname.startswith(StagedMetaFinder.STAGED_PREFIX)
