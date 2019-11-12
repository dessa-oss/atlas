"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.v1.models.data_contract_details import DataContractDetails


class TestDataContractDetails(Spec):

    @let_now
    def redis_connection(self):
        import fakeredis
        return self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @let
    def data_contract_uuid(self):
        return self.faker.uuid4()

    @staticmethod
    def _key_to_write(uuid):
        return f'contracts:{uuid}:info'

    def _write_summary_to_redis(self, uuid, details):
        key_to_write = self._key_to_write(uuid)
        self.redis_connection.set(key_to_write, details)

    @set_up
    def set_up(self):
        self.redis_connection.flushall()

    def test_data_contract_details_returns_none_if_uuid_not_in_redis(self):
        promise = DataContractDetails.get(self.data_contract_uuid)
        self.assertIsNone(promise.evaluate())

    def test_data_contract_details_returns_info_if_uuid_in_redis(self):
        data_contract_info = str(self.faker.pydict())

        self._write_summary_to_redis(self.data_contract_uuid, data_contract_info)

        promise = DataContractDetails.get(self.data_contract_uuid)

        self.assertEqual(data_contract_info, promise.evaluate())
