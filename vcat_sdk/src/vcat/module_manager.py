class ModuleManager(object):

    def __init__(self):
        import vcat
        self._module_listing = []

    def append_module(self, module):
        print(module)
        self._module_listing.append(module)