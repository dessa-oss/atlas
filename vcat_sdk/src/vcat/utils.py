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
    digest.update(string)
    return digest.hexdigest()


def merged_uuids(uuids):
    from hashlib import sha1
    digest = sha1()
    for uuid in uuids:
        digest.update(uuid)
    return digest.hexdigest()


def make_uuid(item, iterable_callback):
    if isinstance(item, list):
        return merged_uuids([iterable_callback(sub_item) for sub_item in item])

    if isinstance(item, basestring):
        return generate_uuid(item)

    return generate_uuid(str(item))

def tgz_archive_without_extension(archive_path):
    return archive_path[0:-4]
