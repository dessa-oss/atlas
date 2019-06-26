"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestCanLoadParameters(Spec):

    @let
    def job_parameters(self):
        import json
        with open(self.script_directory + '/foundations_job_parameters.json', 'r') as file:
            return json.load(file)

    @let
    def script_directory(self):
        return 'acceptance/fixtures/script_parameters'

    def test_can_load_parameters_within_python(self):
        from foundations_internal.change_directory import ChangeDirectory
        import subprocess
        import json

        with ChangeDirectory(self.script_directory):
            completed_process = subprocess.run(['python', 'main.py'], stdout=subprocess.PIPE)
            process_output = completed_process.stdout

        result_parameters = json.loads(process_output)
        self.assertEqual(self.job_parameters, result_parameters)