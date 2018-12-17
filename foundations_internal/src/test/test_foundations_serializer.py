"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch, Mock

import foundations_internal.foundations_serializer as serializer

class TestFoundationsSerializer(unittest.TestCase):

    def test_serialize_saves_magic(self):
        import pickle

        magic = serializer.serialize('A')[:4]
        self.assertEqual(b'FNDS', magic)

    def test_serialize_can_serialize_pickle_with_header(self):
        import pickle

        serialized_data = serializer.serialize('A')[4:]
        self.assertEqual('A', pickle.loads(serialized_data))

    def test_serialize_can_serialize_pickle_with_header_different_value(self):
        import pickle

        serialized_data = serializer.serialize(Exception)[4:]
        self.assertEqual(Exception, pickle.loads(serialized_data))

    def test_dumps_is_serialize(self):
        self.assertEqual(serializer.serialize, serializer.dumps)

    def test_deserialize_can_load_serialized_data(self):
        serialized_data = serializer.serialize('A')
        self.assertEqual('A', serializer.deserialize(serialized_data))

    def test_deserialize_can_load_serialized_data_different_value(self):
        serialized_data = serializer.serialize(9.34343)
        self.assertEqual(9.34343, serializer.deserialize(serialized_data))

    def test_deserialize_can_load_json(self):
        import json

        serialized_data = json.dumps({'hello': 'world'})
        self.assertEqual({'hello': 'world'}, serializer.deserialize(serialized_data))

    def test_deserialize_can_load_json_different_value(self):
        import json

        serialized_data = json.dumps({'world': 'hello'})
        self.assertEqual({'world': 'hello'}, serializer.deserialize(serialized_data))

    @patch('json.loads')
    def test_deserialize_can_decode_json_bytes(self, json_mock):
        json_mock.side_effect = lambda input: input

        serialized_data = b'some binary json'
        self.assertEqual('some binary json', serializer.deserialize(serialized_data))

    def test_deserialize_can_load_none_as_none(self):
        self.assertEqual(None, serializer.deserialize(None))

    def test_loads_is_deserialize(self):
        self.assertEqual(serializer.deserialize, serializer.loads)
