

class ScriptEnvironment(object):
    def __init__(self, config):
        self._config = config

    def write_environment(self, file):
        from pipes import quote

        for name, value in self._run_script_environment().items():
            file.write("export {}={}\n".format(quote(name), quote(str(value))))
        file.flush()
        file.seek(0)

    def _run_script_environment(self):
        return self._config.get("run_script_environment", {})
