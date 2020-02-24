

class ModuleManager(object):

    def __init__(self):
        self._module_listing = []

    def append_module(self, module):
        reference = {
            'name': module.__name__,
            'directory': self._module_directory(module),
        }
        self._module_listing.append(reference)

    def module_directories_and_names(self):
        for module in self._module_listing:
            yield module['name'], module['directory']

    def _module_directory(self, module):
        import os
        from os.path import abspath

        module_directory = os.path.dirname(module.__file__)
        return abspath(module_directory)
