"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

class PackagePool(object):
    def __init__(self, active_package_limit):
        self._model_packages = {}
        self._active_packages = []
        self._active_package_limit = active_package_limit
    
    def _remove_process_from_pool(self):
        process_to_kill = self._active_packages[0]
        self._active_packages.pop(0)
        self._model_packages[process_to_kill]['process'].close()

    def add_package(self, model_id):
        from foundations_production.serving.restartable_process import RestartableProcess
        from foundations_production.serving.package_runner import run_model_package

        if len(self._model_packages) >= self._active_package_limit:
            self._remove_process_from_pool()

        process = RestartableProcess(target=run_model_package, args=(model_id))
        pipe = process.start()
        self._model_packages[model_id] = {'pipe': pipe, 'process': process}
        self._active_packages.append(model_id)

    def get_pipe(self, model_id):
        model_package = self._model_packages.get(model_id, None)

        if not model_package:
            return None

        if model_id not in self._active_packages:
            if len(self._model_packages) >= self._active_package_limit:
                self._remove_process_from_pool()

            updated_model_pipe = model_package['process'].start()
            model_package['pipe'] = updated_model_pipe
            self._active_packages.append(model_id)

        return model_package['pipe']
