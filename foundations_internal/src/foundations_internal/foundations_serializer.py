import foundations_internal.fast_serializer as pickle_serializer
from foundations.utils import string_from_bytes
import json

HEADER_MAGIC = b'FNDS'

def serialize(value):
    return HEADER_MAGIC + pickle_serializer.serialize(value)

dumps = serialize

def deserialize(serialized_value):

    if serialized_value is None:
        return None

    magic = serialized_value[:4]
    if magic == HEADER_MAGIC:
        return pickle_serializer.deserialize(serialized_value[4:])
    else:
        decoded_json = string_from_bytes(serialized_value)
        return json.loads(decoded_json)

loads = deserialize