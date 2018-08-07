"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import vcat
import config
from staged_common.data import load_titanic
from staged_common.prep import require
from staged_common.logging import log_data

def main():
    # defining the stage twice while explicitly enabling caching will prevent the method from running twice
    data = 'hello world'
    log = log_data(data)
    log.enable_caching()

    log2 = log_data(data)
    log2.enable_caching()
    
    executor = require(log, log2)
    executor.run_same_process()

if __name__ == '__main__':
    main()