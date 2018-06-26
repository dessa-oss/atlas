"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from vcat.job import Job

class DummyPipeline(object):
    def __init__(self, func):
        self._func = func
        self._pipeline_context = "test_context"

    def run_same_process(self, **kwargs):
        return self._func(**kwargs)

    def pipeline_context(self):
        return self._pipeline_context

class TestJob(unittest.TestCase):
    def test_pipeline_context_get(self):
        pipe = DummyPipeline(None)
        self.assertEqual(Job(pipe).pipeline_context(), "test_context")

    def test_run_no_kwargs(self):
        pipe = DummyPipeline(lambda: "asdf")
        job = Job(pipe)

        self.assertEqual(job.run(), "asdf")

    def test_run_full_kwargs(self):
        pipe = DummyPipeline(lambda x, y: x + y)
        job = Job(pipe, x=5, y=6)

        self.assertEqual(job.run(), 11)

    def test_run_missing_kwargs(self):
        pipe = DummyPipeline(lambda x, y, z: x + y - z)
        job = Job(pipe, x=6, z=11)

        try:
            job.run()
            self.fail("Job should have failed")
        except TypeError as e:
            self.assertEqual(str(e), "<lambda>() takes exactly 3 arguments (2 given)")
        except:
            self.fail("Caught wrong exception")

    def test_run_unused_kwargs(self):
        pipe = DummyPipeline(lambda x, y, z: x + y - z)
        job = Job(pipe, x=6, y=7, z=8, w=100)

        try:
            job.run()
            self.fail("Job should have failed")
        except TypeError as e:
            self.assertEqual(str(e), "<lambda>() got an unexpected keyword argument 'w'")
        except:
            self.fail("Caught wrong exception")

    def test_serialize_deserialize(self):
        def test_func(x, y, z):
            return x + y - z

        job = Job(DummyPipeline(test_func), x=5, y=6, z=7)

        serialized = job.serialize()
        deserialized_job = Job.deserialize(serialized)

        self.assertEqual(deserialized_job.run(), job.run())
        self.assertEqual(deserialized_job.pipeline_context(), job.pipeline_context())