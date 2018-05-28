import os
import random


class Provenance(object):

    # - env variables for configuration
    # - Bundled files (source code)
    #     - Code
    #     - Config files
    #     - Data files
    # - 'Pip freeze' for versioning
    # - Seed
    # - Config
    # - tags

    def __init__(self):
        self.job_bundle = None
        self.environment = {}
        self.config = {}
        self.tags = []
        self.random_state = None
        self.module_versions = {}
        self.pip_freeze = None

    def fill_config(self):
        import yaml

        file_list = self.job_bundle.get_files('*.config.yaml')
        for bundled_file in file_list:
            with bundled_file.open('r') as file:
                self.config.update(yaml.load(file))        

    def fill_environment(self):
        for key, value in os.environ.items():
            self.environment[key] = value

    def fill_random_state(self):
        self.random_state = random.getstate()

    def fill_pip_modules(self):
        import subprocess

        reader, writer = os.pipe()
        subprocess.call(['python', '-m', 'pip', 'freeze'], stdout=writer)
        self.pip_freeze = os.read(reader, 65536).strip()
        split_lines = [line.split('==') for line in self.pip_freeze.split("\n")]
        versioned_lines = filter(lambda line: len(line) == 2, split_lines)
        self.module_versions = dict(versioned_lines)
