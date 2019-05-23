"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class FoundationsContext(object):
    """The global state for all staging related functionality for Foundations.
    This is where everything awesome begins!!!

    Arguments:
        pipeline {Pipeline} -- The initial Foundation pipeline to use for stages
    """

    class ChangePipeline(object):

        def __init__(self, context, pipeline):
            self._context = context
            self._pipeline = pipeline
            self._previous_pipeline = None

        def __enter__(self):
            self._previous_pipeline = self._context._pipeline
            self._context._pipeline = self._pipeline

        def __exit__(self, exception_type, exception_value, traceback):
            self._context._pipeline = self._previous_pipeline

    def __init__(self, pipeline):
        from foundations_internal.job_resources import JobResources

        self._pipeline = pipeline
        self._job_resources = JobResources(0, None)

    def pipeline(self):
        """The current pipeline used for all staging functionality in Foundations

        Returns:
            Pipeline -- As above
        """

        return self._pipeline

    def pipeline_context(self):
        """The current pipeline context associate with the assigned pipeline

        Returns:
            PipelineContext -- As above
        """

        return self._pipeline.pipeline_context()

    def change_pipeline(self, new_pipeline):
        """Replaces the pipeline entrypoint for stages within a with block
        and then resets it upon exitting
        
        Arguments:
            new_pipeline {Pipeline} -- The pipeline to set
        
        Returns:
            ChangePipeline -- The class to implement the above functionality
        """

        return self.ChangePipeline(self, new_pipeline)

    def __getstate__(self):
        raise ValueError('FoundationsContexts do not support serialization')

    def __setstate__(self, state):
        raise ValueError('FoundationsContexts do not support serialization')

    def set_project_name(self, project_name):
        self.pipeline_context().provenance.project_name = project_name

    def job_id(self):
        return self.pipeline_context().file_name

    def job_resources(self):
        return self._job_resources

    def set_job_resources(self, job_resources):
        self._job_resources = job_resources