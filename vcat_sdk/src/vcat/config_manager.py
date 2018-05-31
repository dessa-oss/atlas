class ConfigManager(object):

    def __init__(self):
        self._config = None

    def config(self):
        if self._config is None:
            self._load()
        return self._config

    def _load(self):
        from vcat.local_directory import LocalDirectory
        import yaml

        config = {}

        directory = LocalDirectory()
        file_list = directory.get_files('*.config.yaml')
        for bundled_file in file_list:
            with bundled_file.open('r') as file:
                config.update(yaml.load(file))

        self._config = config
