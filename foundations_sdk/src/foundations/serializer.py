"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def serialize(item):
    import dill as pickle
    return pickle.dumps(item, protocol=2)


def deserialize(serialized_item):
    try:
        import dill as pickle
        return None if serialized_item is None else pickle.loads(serialized_item)
    except ValueError:
        return None


def serialize_to_file(item, file):
    import dill as pickle
    return pickle.dump(item, file, protocol=2)


def deserialize_from_file(file):
    try:
        import dill as pickle
        return None if file is None else pickle.load(file)
    except ValueError:
        return None
