def serialize(item):
    import dill as pickle
    return pickle.dumps(item)


def deserialize(serialized_item):
    try:
        import dill as pickle
        return None if serialized_item is None else pickle.loads(serialized_item)
    except ValueError:
        return None


def serialize_to_file(item, file):
    import dill as pickle
    return pickle.dump(item, file)


def deserialize_from_file(file):
    try:
        import dill as pickle
        return None if file is None else pickle.load(file)
    except ValueError:
        return None
