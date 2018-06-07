def file_archive_name(prefix, name):
    if prefix is not None:
        return prefix + '/' + name
    else:
        return name


def file_archive_name_with_additional_prefix(prefix, additional_prefix, name):
    return file_archive_name(prefix, additional_prefix + '/' + name)


def generate_uuid(string):
    from hashlib import sha1
    digest = sha1()
    digest.update(string.encode('utf-8'))
    return digest.hexdigest()


def merged_uuids(uuids):
    from hashlib import sha1
    digest = sha1()
    for uuid in uuids:
        digest.update(uuid.encode('utf-8'))
    return digest.hexdigest()


def make_uuid(item, iterable_callback):
    if isinstance(item, list):
        return merged_uuids([iterable_callback(sub_item) for sub_item in item])

    if isinstance(item, str):
        return generate_uuid(item)

    return generate_uuid(str(item))

def tgz_archive_without_extension(archive_path):
    return archive_path[0:-4]

def _list_items(arr):
    for i in range(len(arr)):
        yield i, arr[i]

def dict_like_iter(dict_like):
    from collections import Iterable

    if isinstance(dict_like, dict):
        return dict_like.items()

    if isinstance(dict_like, Iterable):
        return _list_items(dict_like)

    return []
    
def dict_like_append(dict_like, key, val):
    from collections import Iterable
        
    if isinstance(dict_like, dict):
        dict_like[key] = val

    if isinstance(dict_like, Iterable):
        dict_like.append(val)

def pretty_time(timestamp):
    import datetime

    try:
        return datetime.datetime.fromtimestamp(timestamp)
    except:
        return timestamp

def restructure_headers(all_headers, first_headers):
    def diff(list_0, list_1):
        set_1 = set(list_1)
        return [item for item in list_0 if item not in set_1]

    return first_headers + diff(all_headers, first_headers)