"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.cache import Cache
from foundations.fast_serializer import serialize, deserialize

class TestCache(unittest.TestCase):
    def setUp(self):
        self.backend = MockBackend()
        self.cache = Cache(self.backend)

    def test_get_metadata_option_object_does_not_exist(self):
        metadata = self.cache.get_metadata_option("cache_uuid")
        self.assertIsNone(metadata.get_or_else(None))

    def test_get_metadata_option_object_exists_metadata_empty(self):
        metadata_to_set = serialize({})
        self.backend.set("cache-uuid", "cached_value", metadata_to_set)

        metadata = self.cache.get_metadata_option("cache-uuid")
        self.assertEqual(metadata.get(), {})

    def test_get_metadata_option_object_exists_metadata_has_one_entry(self):
        metadata_to_set = serialize({"job_id": "asdf"})
        self.backend.set("cache-uuid", serialize("cached_value"), metadata_to_set)

        metadata = self.cache.get_metadata_option("cache-uuid")
        self.assertEqual(metadata.get(), {"job_id": "asdf"})

    def test_get_metadata_option_object_exists_metadata_has_two_entries(self):
        metadata_to_set = serialize({"job_id": "asdf", "ser_vers": 3})
        self.backend.set("cache-uuid", serialize("cached_value"), metadata_to_set)

        metadata = self.cache.get_metadata_option("cache-uuid")
        self.assertEqual(metadata.get(), {"job_id": "asdf", "ser_vers": 3})

    def test_get_metadata_option_object_exists_metadata_has_two_entries_different_object(self):
        metadata_to_set = serialize({"job_id": "asdf", "ser_vers": 3})
        self.backend.set("cache-uuid2", serialize("cached_value"), metadata_to_set)

        metadata = self.cache.get_metadata_option("cache-uuid2")
        self.assertEqual(metadata.get(), {"job_id": "asdf", "ser_vers": 3})

    def test_set_no_flags(self):
        self.cache.set("asdf", None, {})
        flags = self.backend._store["asdf"].flags
        self.assertEqual(flags, {})

    def test_set_one_flag(self):
        self.cache.set("asdf", None, {}, flag1=1)
        flags = self.backend._store["asdf"].flags
        self.assertEqual(flags, {"flag1": 1})

    def test_set_two_flags(self):
        self.cache.set("asdf", None, {}, flag1=1, flag2=2)
        flags = self.backend._store["asdf"].flags
        self.assertEqual(flags, {"flag1": 1, "flag2": 2})

    def test_set_object_no_metadata(self):
        self.cache.set("asdf", 222, {})

        data = self.backend.get("asdf")
        metadata = self.backend.get_metadata("asdf")

        self.assertEqual(data, serialize(222))
        self.assertEqual(metadata, serialize({}))

    def test_set_object_some_metadata(self):
        self.cache.set("asdf", "dfdd", {"job": "job_id"})

        data = self.backend.get("asdf")
        metadata = self.backend.get_metadata("asdf")
        
        self.assertEqual(data, serialize("dfdd"))
        self.assertEqual(metadata, serialize({"job": "job_id"}))

    def test_set_object_more_metadata(self):
        self.cache.set("another", [1, 2, 3], {"job": "job_id", "de_ver": 3})

        data = self.backend.get("another")
        metadata = self.backend.get_metadata("another")
        
        self.assertEqual(data, serialize([1, 2, 3]))
        self.assertEqual(metadata, serialize({"job": "job_id", "de_ver": 3}))

    def test_simple_round_trip_no_metadata(self):
        self.cache.set("asdf", 222, {})
        data = self.cache.get_option("asdf")
        self.assertEqual(data.get(), 222)

    def test_simple_round_trip2_no_metadata(self):
        self.cache.set("asdf", "dfsdfsdfdf", {})
        data = self.cache.get_option("asdf")
        self.assertEqual(data.get(), "dfsdfsdfdf")

    def test_simple_round_trip2_with_metadata(self):
        self.cache.set("asdf", "dfsdfsdfdf", {"job": "job_id", "another": "yes"})

        data = self.cache.get_option("asdf")
        metadata = self.cache.get_metadata_option("asdf")

        self.assertEqual(data.get(), "dfsdfsdfdf")
        self.assertEqual(metadata.get(), {"job": "job_id", "another": "yes"})

class MockBackend(object):
    class Container(object):
        def __init__(self):
            self.object = None
            self.metadata = None
            self.flags = {}

    def __init__(self):
        self._store = {}

    def _safely_get(self, cache_uuid, callback):
        container = self._store.get(cache_uuid)
        if container:
            return callback(container)
        else:
            return None

    def get(self, cache_uuid):
        return self._safely_get(cache_uuid, lambda container: container.object)

    def get_metadata(self, cache_uuid):
        return self._safely_get(cache_uuid, lambda container: container.metadata)

    def set(self, cache_uuid, to_store, metadata, **flags):
        container = self.Container()
        container.object = to_store
        container.metadata = metadata
        container.flags = flags
        
        self._store[cache_uuid] = container
