"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def _install():
    import sys
    from vcat.staged_meta_finder import StagedMetaFinder
    sys.meta_path.insert(0, StagedMetaFinder())


_install()
