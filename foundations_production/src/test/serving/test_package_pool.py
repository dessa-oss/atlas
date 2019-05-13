"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_production.serving.package_pool import PackagePool
from foundations_production.serving.package_runner import run_model_package

class TestPackagePool(Spec):

    model_1_new_communicator = let_mock()

    @let
    def model_id(self):
        return self.faker.uuid4()

    @let
    def model_2_id(self):
        return self.faker.uuid4()
    
    @let
    def model_3_id(self):
        return self.faker.uuid4()
    @let
    def fake_data(self):
        import pandas
        return pandas.DataFrame({self.faker.word(): self.faker.words()})
    
    @set_up
    def set_up(self):
        self.mock_process = self.patch('foundations_production.serving.restartable_process.RestartableProcess', ConditionalReturn())
        self.model_1_process, self.model_1_communicator = self._create_new_model_process(self.model_id)
        self.model_2_process, self.model_2_communicator = self._create_new_model_process(self.model_2_id)
        self.model_3_process, self.model_3_communicator = self._create_new_model_process(self.model_3_id)
        self.model_1_process.start.side_effect = [self.model_1_communicator, self.model_1_new_communicator]

    def _create_new_model_process(self, model_id):
        model_process = Mock()
        model_communicator = Mock()

        self.mock_process.return_when(model_process, target=run_model_package, args=(model_id,))
        model_process.start.return_value = model_communicator

        return model_process, model_communicator

    def test_package_pool_add_package_creates_new_process(self):
        package_pool = PackagePool(active_package_limit=1)
        package_pool.add_package(self.model_id)
        self.mock_process.assert_called_with(target=run_model_package, args=(self.model_id,))
        
    def test_package_pool_does_not_exceed_limit(self):
        package_pool = PackagePool(active_package_limit=2)
        package_pool.add_package(self.model_id)
        package_pool.add_package(self.model_2_id)
        package_pool.add_package(self.model_3_id)
        self.model_1_process.terminate.assert_called_once()
        self.model_2_process.terminate.assert_not_called()
    
    def test_package_pool_does_not_close_not_active_process(self):
        package_pool = PackagePool(active_package_limit=1)
        package_pool.add_package(self.model_id)
        package_pool.add_package(self.model_2_id)
        package_pool.add_package(self.model_3_id)
        self.model_1_process.terminate.assert_called_once()
    
    def test_get_communicator_gets_correct_communicator(self):
        package_pool = PackagePool(active_package_limit=1)
        package_pool.add_package(self.model_id)
        self.assertEqual(self.model_1_communicator, package_pool.get_communicator(self.model_id))

    def test_get_communicator_returns_none_when_model_doesnt_exist(self):
        package_pool = PackagePool(active_package_limit=1)
        self.assertEqual(None, package_pool.get_communicator(self.model_id))
    
    def test_get_communicator_starts_process_if_inactive(self):
        package_pool = PackagePool(active_package_limit=1)
        package_pool.add_package(self.model_id)
        package_pool.add_package(self.model_2_id)
        package_pool.get_communicator(self.model_id)
        self.assertEqual(2, self.model_1_process.start.call_count)
    
    def test_get_communicator_does_not_starts_process_if_active(self):
        package_pool = PackagePool(active_package_limit=1)
        package_pool.add_package(self.model_id)
        package_pool.get_communicator(self.model_id)
        self.model_1_process.start.assert_called_once()
    
    def test_get_communicator_does_starts_process_once_if_inactive(self):
        package_pool = PackagePool(active_package_limit=1)
        package_pool.add_package(self.model_id)
        package_pool.add_package(self.model_2_id)
        package_pool.get_communicator(self.model_id)
        package_pool.get_communicator(self.model_id)

        self.assertEqual(2, self.model_1_process.start.call_count)
    
    def test_get_communicator_does_not_exceed_active_process_limit(self):
        package_pool = PackagePool(active_package_limit=1)
        package_pool.add_package(self.model_id)
        package_pool.add_package(self.model_2_id)
        package_pool.get_communicator(self.model_id)

        self.model_2_process.terminate.assert_called_once()
    
    def test_get_communicator_updates_stored_communicator_when_process_restarted(self):
        package_pool = PackagePool(active_package_limit=1)
        package_pool.add_package(self.model_id)
        package_pool.add_package(self.model_2_id)
        communicator = package_pool.get_communicator(self.model_id)
        self.assertEqual(self.model_1_new_communicator, communicator)

