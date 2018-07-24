"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def _install():
    import sys
    if sys.version_info[0] < 3:
        from foundations.staged_meta_py2_finder import StagedMetaPy2Finder
        sys.meta_path.append(StagedMetaPy2Finder())
    else:
        from foundations.staged_meta_finder import StagedMetaFinder
        sys.meta_path.insert(0, StagedMetaFinder())


_install()
