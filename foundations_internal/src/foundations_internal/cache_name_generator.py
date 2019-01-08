"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class CacheNameGenerator(object):

    def __init__(self, stage, live_arguments):
        self._stage = stage
        self._live_arguments = live_arguments

    def hash(self):
        from sys import version_info
        from foundations.utils import merged_uuids, make_uuid

        argument_hashes = [argument.hash()
                           for argument in self._live_arguments]
        argument_hash = merged_uuids(argument_hashes)

        version_hash = make_uuid(version_info.major, make_uuid)

        return merged_uuids([argument_hash, version_hash, self._stage.uuid()])
