import unittest


class TestPipelineInterface(unittest.TestCase):
    def test_pipeline_interface(self):
        from staged_acceptance.fixtures.stages import *
        import acceptance.fixtures.stages as stages
        from vcat import Hyperparameter, Job, JobSourceBundle, deployment_manager, wait_for_deployment_to_complete
        
        previous_stage = bundle_value(5)
        stage = add(previous_stage, Hyperparameter("b"))
        stage.persist()

        job = Job(stage, b=4)
        job_source_bundle = JobSourceBundle('test_job_bundle', '../')
        deployment = deployment_manager.deploy({}, 'test_job', job, job_source_bundle)

        wait_for_deployment_to_complete(deployment)
        result = deployment.fetch_job_results()

        self.assertEqual(result['stage_contexts'][stage.uuid()]['stage_output'], 9)

