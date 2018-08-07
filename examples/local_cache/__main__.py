"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
The purpose of this module is to show what happens when you have redundant execution.
When a stage is defined and invoked more than once in a single job, its result will be
cached in memory for the lifetime of that job so that it is not recomputed unnecessarily.
The main use case for this is if you have a larger dataset or some result that is computationally
expensive and you wish to use it more than once.

If you execute this module, you will see 'hello world' printed twice - this is because even
though log_data is defined already, it is being called directly twice.  When wrapping your code
via import with the "staged_" prefix, your function is changed to return a handle that performs
the in-memory caching.  Since there are two handles, there will be two executions for log_data.

On the other hand 'bye bye' will be printed exactly once.  Since log_data is called only once,
but the handle is reused, the stage will only be executed once.

The main takeaway is that you will most likely want to call a stage function only once and reuse
the result as needed.
"""

import foundations
import config
from staged_common.data import load_titanic
from staged_common.prep import require
from staged_common.logging import log_data

def main():
    # redefining the stage twice will not cache the data
    data = 'hello world'
    log = log_data(data)
    log2 = log_data(data)
    executor = require(log, log2)
    executor.run_same_process()

    # however, reusing the same stage will cache the data
    data = 'bye bye'
    log = log_data(data)
    executor = require(log, log)
    executor.run_same_process()

if __name__ == '__main__':
    main()