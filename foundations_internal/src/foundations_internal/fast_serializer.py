"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def _pick_module():
    try:
        import cPickle as pickle
    except ImportError:
        import pickle
    return pickle

pickle = _pick_module()

def serialize(item):
    return pickle.dumps(item, protocol=4)

def deserialize(serialized_item):
    try:
        return None if serialized_item is None else pickle.loads(serialized_item)
    except ValueError:
        return None


def serialize_to_file(item, file):
    return pickle.dump(item, file, protocol=2)


def deserialize_from_file(file):
    try:
        return None if file is None else pickle.load(file)
    except ValueError:
        return None
