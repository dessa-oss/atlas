"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def serialize(item):
    import dill
    return dill.dumps(item, protocol=2, recurse=True)


def deserialize(serialized_item):
    try:
        import dill
        _fix_dill()
        return None if serialized_item is None else dill.loads(serialized_item)
    except ValueError:
        return None


def serialize_to_file(item, file):
    import dill as pickle
    return pickle.dump(item, file, protocol=2, recurse=True)


def deserialize_from_file(file):
    try:
        import dill
        _fix_dill()
        return None if file is None else dill.load(file)
    except ValueError:
        return None

def _fix_dill():
    import dill
    dill._dill._reverse_typemap['ClassType'] = type