import os
import random

from vcat.local_directory import LocalDirectory
from vcat.stage_hierarchy import StageHierarchy

class Provenance(object):

    def __init__(self):
        self.job_source_bundle = None
        self.environment = {}
        self.config = {}
        self.tags = []
        self.random_state = None
        self.module_versions = {}
        self.pip_freeze = None
        self.stage_hierarchy = StageHierarchy()

    def save_to_archive(self, archiver):
        archiver.append_provenance(self._archive_provenance())
        if self.job_source_bundle is not None:
            archiver.append_job_source(self.job_source_bundle.job_archive())

    def load_from_archive(self, archiver):
        archive_provenance = archiver.fetch_provenance()
        self._load_archive_provenance(archive_provenance)
        if self.job_source_bundle is not None:
            archiver.fetch_job_source(self.job_source_bundle.job_archive())

    def fill_all(self):
        self.fill_config()
        self.fill_environment()
        self.fill_random_state()
        self.fill_pip_modules()

    def fill_config(self):
        import yaml

        directory = LocalDirectory()
        file_list = directory.get_files('*.config.yaml')
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
        split_lines = [line.split('==')
                       for line in self.pip_freeze.split("\n")]
        versioned_lines = filter(lambda line: len(line) == 2, split_lines)
        self.module_versions = dict(versioned_lines)

    def _archive_provenance(self):
        return {
            "environment": self.environment,
            "config": self.config,
            "tags": self.tags,
            "random_state": self.random_state,
            "module_versions": self.module_versions,
            "pip_freeze": self.pip_freeze,
            "stage_hierarchy": self.stage_hierarchy
        }

    def _load_archive_provenance(self, archive_provenance):
        self.environment = archive_provenance["environment"]
        self.config = archive_provenance["config"]
        self.tags = archive_provenance["tags"]
        self.random_state = archive_provenance["random_state"]
        self.module_versions = archive_provenance["module_versions"]
        self.pip_freeze = archive_provenance["pip_freeze"]
        self.stage_hierarchy = archive_provenance["stage_hierarchy"]