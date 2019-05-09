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

    def add_package(self, model_id):
        from foundations_production.serving.restartable_process import RestartableProcess
        from foundations_production.serving.package_runner import run_model_package

        self._remove_process_from_pool_if_limit_exceeded()

        process = RestartableProcess(target=run_model_package, args=(model_id))
        ipc = process.start()

        self._model_packages[model_id] = {'ipc': ipc, 'process': process}
        self._active_packages.append(model_id)

    def get_ipc(self, model_id):
        model_package = self._model_packages.get(model_id, None)

        if not model_package:
            return None

        if model_id not in self._active_packages:
            self._restart_process_and_update_ipc(model_package, model_id)

        return model_package['ipc']
    
    def _remove_process_from_pool_if_limit_exceeded(self):
        if len(self._model_packages) >= self._active_package_limit:
            process_to_kill = self._active_packages[0]
            self._active_packages.pop(0)
            self._model_packages[process_to_kill]['process'].close()
    
    def _restart_process_and_update_ipc(self, model_package, model_id):
        self._remove_process_from_pool_if_limit_exceeded()
        
        updated_model_ipc = model_package['process'].start()
        model_package['ipc'] = updated_model_ipc
        self._active_packages.append(model_id)
