"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import foundations
from staged_common.data import load_titanic
from staged_common.prep import get_mode, fillna
from staged_common.logging import log_data

if __name__ == '__main__':
    data = load_titanic()
    mode = get_mode(data, 'Cabin')
    data = fillna(data, 'Cabin', mode)
    log_data(data).run()
