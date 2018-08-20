"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import os
import random

from foundations.local_directory import LocalDirectory
from foundations.stage_hierarchy import StageHierarchy


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
        self.python_version = None

    def fill_python_version(self):
        import sys
        self.python_version = {
            "major": sys.version_info.major,
            "minor": sys.version_info.minor,
            "micro": sys.version_info.micro,
            "releaselevel": sys.version_info.releaselevel,
            "serial": sys.version_info.serial,
        }

    def save_to_archive(self, archiver):
        archiver.append_provenance(self._archive_provenance())
        if self.job_source_bundle is not None:
            archiver.append_job_source(self.job_source_bundle.job_archive())

    def load_stage_log_from_archive(self, archiver):
        pass

    def load_persisted_data_from_archive(self, archiver):
        pass

    def load_provenance_from_archive(self, archiver):
        archive_provenance = archiver.fetch_provenance() or {}
        self._load_archive_provenance(archive_provenance)

    def load_job_source_from_archive(self, archiver):
        if self.job_source_bundle is not None:
            archiver.fetch_job_source(self.job_source_bundle.job_archive())

    def load_artifact_from_archive(self, archiver):
        pass

    def load_miscellaneous_from_archive(self, archiver):
        pass

    def fill_all(self, config_manager):
        self.fill_python_version()
        self.fill_config(config_manager)
        self.fill_environment()
        self.fill_random_state()
        self.fill_pip_modules()

    def fill_config(self, config_manager):
        self.config.update(config_manager.config())

    def fill_environment(self):
        for key, value in os.environ.items():
            self.environment[key] = value

    def fill_random_state(self):
        self.random_state = random.getstate()

    # TODO: look into better way to test pip modules
    def fill_pip_modules(self):
        import subprocess
        from foundations.utils import string_from_bytes

        reader, writer = os.pipe()
        subprocess.call(['python', '-m', 'pip', 'freeze'], stdout=writer)
        pip_freeze_string = string_from_bytes(os.read(reader, 65536))
        self.pip_freeze = pip_freeze_string.strip()
        split_lines = [line.split('==') for line in self.pip_freeze.split("\n")]
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
            "stage_hierarchy": self.stage_hierarchy,
            "python_version": self.python_version
        }

    def _load_archive_provenance(self, archive_provenance):
        self.environment = archive_provenance.get(
            "environment", self.environment)
        self.config = archive_provenance.get("config", self.config)
        self.tags = archive_provenance.get("tags", self.tags)
        self.random_state = archive_provenance.get(
            "random_state", self.random_state)
        self.module_versions = archive_provenance.get(
            "module_versions", self.module_versions)
        self.pip_freeze = archive_provenance.get("pip_freeze", self.pip_freeze)
        self.stage_hierarchy = archive_provenance.get(
            "stage_hierarchy", self.stage_hierarchy)
        self.python_version = archive_provenance.get(
            "python_version", self.python_version)
