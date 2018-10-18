"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 10 2018
"""

import unittest
from mock import patch

import integration.fixtures.stages as stages

from foundations import config_manager, create_stage, JobPersister, ResultReader
from foundations.job import Job

class TestPersistUnserializableData(unittest.TestCase):
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

        job = TestPersistUnserializableData._run_and_persist_job(stage_output)
        pipeline_context = job.pipeline_context()
        job_name = pipeline_context.file_name

        stage_uuid = TestPersistUnserializableData._lookup_stage_uuid_from_name(pipeline_context, "returns_generator")

        result_reader = TestPersistUnserializableData._create_result_reader()

        self._successfully_try_and_fail_to_get_results(
            result_reader,
            job_name,
            "returns_generator",
            stage_uuid
        )

    def test_try_persist_generator_and_pass_to_next_stage_and_retrieve_results(self):
        returns_fresh_generator = create_stage(stages.returns_fresh_generator)
        executes_generator = create_stage(stages.executes_generator)

        gen = returns_fresh_generator().persist()
        value = executes_generator(gen).persist()

        job = TestPersistUnserializableData._run_and_persist_job(value)
        pipeline_context = job.pipeline_context()
        job_name = pipeline_context.file_name

        uuid_for_good_stage = TestPersistUnserializableData._lookup_stage_uuid_from_name(
            pipeline_context,
            "executes_generator"
        )

        uuid_for_bad_stage = TestPersistUnserializableData._lookup_stage_uuid_from_name(
            pipeline_context,
            "returns_fresh_generator"
        )

        result_reader = TestPersistUnserializableData._create_result_reader()

        self._successfully_try_and_fail_to_get_results(
            result_reader,
            job_name,
            "returns_fresh_generator",
            uuid_for_bad_stage
        )

        generator_value = result_reader.get_unstructured_results(job_name, [uuid_for_good_stage])[0]
        self.assertEqual(generator_value, "beep")

    @staticmethod
    def _lookup_stage_uuid_from_name(pipeline_context, stage_name):
        provenance = pipeline_context.provenance
        stage_hierarchy_entries = provenance.stage_hierarchy.entries
        
        for stage_uuid, entry in stage_hierarchy_entries.items():
            if entry.function_name == stage_name:
                return stage_uuid

        return None

    def _successfully_try_and_fail_to_get_results(self, result_reader, job_name, stage_name, stage_uuid):
        try:
            result_reader.get_unstructured_results(job_name, [stage_uuid])
            self.fail("should have thrown a type error")
        except TypeError as e:
            format_string = "Was not able to serialize output for stage '{}' for job '{}' (stage uuid: {})."
            expected_error_message = format_string.format(stage_name, job_name, stage_uuid)
            self.assertEqual(str(e), expected_error_message)

    @staticmethod
    def _create_result_reader():
        with JobPersister.load_archiver_fetch() as fetch:
            return ResultReader(fetch)

    @staticmethod
    def _run_and_persist_job(stage_to_run):
        job = Job(stage_to_run)
        job.run()

        JobPersister(job).persist()

        return job

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