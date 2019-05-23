"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestResultsFileCreation(Spec):

    @let
    def result_file_path(self):
        import os

        file_path =  os.path.join('results', self.faker.file_path(extension='pkl')[1:])
        return file_path
    
    def test_job_creates_results_file(self):
        from acceptance.fixtures.stages import save_file_with_pickle
        from foundations.global_state import foundations_context

        stage = foundations_context.pipeline().stage(save_file_with_pickle, self.result_file_path)
        stage.persist()
        deployment = stage.run()
        deployment.wait_for_deployment_to_complete()
