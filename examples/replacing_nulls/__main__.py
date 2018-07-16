"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import foundations
import config
from staged_common.data import load_titanic
from staged_common.prep import fillna
from staged_common.logging import log_data

if __name__ == '__main__':
    data = load_titanic()
    data = fillna(data, 'Cabin', 'NULLCABIN')
    data = fillna(data, 'Embarked', 'NULLEMBARKED')
    log_data(data).run()
