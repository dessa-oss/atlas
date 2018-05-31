class ConfigManager(object):

    def __init__(self):
        self.config = {}

    def load(self):
        from vcat.local_directory import LocalDirectory
        import yaml

        directory = LocalDirectory()
        file_list = directory.get_files('*.config.yaml')
        for bundled_file in file_list:
            with bundled_file.open('r') as file:
                self.config.update(yaml.load(file))
