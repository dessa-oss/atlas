"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_internal.testing.helpers import *
from foundations_internal.testing.helpers.spec import Spec

@skip
class TestJobAnnotations(Spec):

    @let
    def job(self):
        import foundations
        return foundations.create_stage(self.stage)()

    @let
    def stage(self):
        def _stage():
            pass
        return _stage

    @let
    def pipeline(self):
        from foundations_internal.pipeline import Pipeline
        return Pipeline(self.pipeline_context)

    @let
    def pipeline_context(self):
        from foundations_internal.pipeline_context import PipelineContext
        return PipelineContext()

    @let
    def annotations(self):
        return {
            'model type': 'simple mlp',
            'data set': 'out of time',
            'what I was doing': 'drinking tea'
        }

    @set_up
    def set_up(self):
        from acceptance.cleanup import cleanup
        from foundations.prototype import set_tag
        from foundations_contrib.global_state import foundations_context

        cleanup()
        foundations_context._pipeline = self.pipeline

        for key, value in self.annotations.items():
            set_tag(key, value)
    
    def test_can_retrieve_job_annotations(self):
        from foundations.prototype import get_metrics_for_all_jobs
        
        self._run_job()

        metrics = get_metrics_for_all_jobs('default')
        job_metrics = metrics[metrics['job_id'] == self.job_id][0]
        self.assertEqual('simple mlp', job_metrics['tag_model type'])
        self.assertEqual('out of time', job_metrics['tag_data set'])
        self.assertEqual('drinking tea', job_metrics['tag_what I was doing'])

    def test_can_retrieve_metrics_in_old_format(self):
        import foundations.prototype
        import foundations
        
        self._run_job()

        prototype_metrics = foundations.prototype.get_metrics_for_all_jobs('default')
        prototype_metrics.drop(['tag_model type', 'tag_data set', 'tag_what I was doing'], inplace=True)
        prototype_job_metrics = prototype_metrics[prototype_metrics['job_id'] == self.job_id][0]
        
        metrics = foundations.get_metrics_for_all_jobs('default')
        job_metrics = metrics[metrics['job_id'] == self.job_id][0]

        self.assertEqual(job_metrics, prototype_job_metrics)

    def _run_job(self):
        deployment = self.job.run()
        self.job_id = deployment.job_name()