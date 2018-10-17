"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 10 2018
"""

import unittest
from mock import patch

import integration.fixtures.stages as stages
from integration.config import integration_config

from foundations import config_manager, create_stage, JobPersister, ResultReader
from foundations.job import Job

class TestPersistUnserializableData(unittest.TestCase):
    def tearDown(self):
        integration_config.cleanup()

    def test_try_persist_generator(self):
        returns_generator = create_stage(stages.returns_generator)
        stage_output = returns_generator().persist()

        job = Job(stage_output)
        job.run()

        with patch('foundations.log_manager', MockLogManager()) as mock_log_manager:
            JobPersister(job).persist()

            warning_messages = mock_log_manager.logger.warning_logs

            generator = stages.returns_generator()
            format_string = "Cannot persist value of type '{}' from stage '{}': {}"
            expected_warning_message = format_string.format("generator", "returns_generator", generator)

            self.assertEqual(len(warning_messages), 1)
            self.assertEqual(warning_messages[0], expected_warning_message)

    def test_try_persist_generator_and_retrieve_results(self):
        returns_generator = create_stage(stages.returns_generator)
        stage_output = returns_generator().persist()

        job = Job(stage_output)
        job.run()

        JobPersister(job).persist()

        with JobPersister.load_archiver_fetch() as fetch:
            result_reader = ResultReader(fetch)

        results_row = result_reader.get_results().iloc[0]
        job_name = results_row["job_name"]
        stage_id = results_row["stage_id"]
        stage_name = results_row["stage_name"]

        try:
            result_reader.get_unstructured_results(job_name, [stage_id])
            self.fail("should have thrown a type error")
        except TypeError as e:
            format_string = "Was not able to serialize output for stage '{}' for job '{}' (stage id: {})."
            expected_error_message = format_string.format(stage_name, job_name, stage_id)
            self.assertEqual(str(e), expected_error_message)

    def test_try_persist_generator_and_pass_to_next_stage_and_retrieve_results(self):
        returns_fresh_generator = create_stage(stages.returns_fresh_generator)
        executes_generator = create_stage(stages.executes_generator)

        gen = returns_fresh_generator().persist()
        value = executes_generator(gen).persist()

        job = Job(value)
        job.run()

        JobPersister(job).persist()

        with JobPersister.load_archiver_fetch() as fetch:
            result_reader = ResultReader(fetch)

        print(result_reader.get_results())

class MockLogManager(object):
    def __init__(self):
        self.logger = MockLogger()

    def get_logger(self, name):
        return self.logger

class MockLogger(object):
    def __init__(self):
        self.warning_logs = []

    def info(self, message):
        pass

    def warning(self, message):
        self.warning_logs.append(message)