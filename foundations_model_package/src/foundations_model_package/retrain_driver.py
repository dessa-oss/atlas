"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class RetrainDriver(object):
    
    def __init__(self, module_name, function_name):
        self._module_name = module_name
        self._function_name = function_name
        self._retrain_driver_file_name = None

    def __enter__(self):
        import random
        
        self._retrain_driver_file_name = f'retrain_driver_{random.randint(0, 1000000)}.py'

        with open(self._retrain_driver_file_name, 'w') as driver_file:
            driver_file.write(self._file_contents())

        return self._retrain_driver_file_name

    def __exit__(self, *args):
        import os
        os.remove(self._retrain_driver_file_name)

    def _file_contents(self):
        file_contents = ''

        file_contents += 'import os\n\n'
        file_contents += 'import foundations\n'
        file_contents += f'from {self._module_name} import {self._function_name}\n\n'
        file_contents += 'params = foundations.load_parameters()\n'
        file_contents += f'{self._function_name}(**params)\n'
        file_contents += f'os.remove({self._retrain_driver_file_name})\n'

        return file_contents