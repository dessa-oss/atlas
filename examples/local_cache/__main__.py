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
though log_data is defined already, it is being called directly twice.  When creating a stage with create_stage(), your function is changed to return a handle that performs
the in-memory caching.  Since there are two handles, there will be two executions for log_data.

On the other hand 'bye bye' will be printed exactly once.  Since log_data is called only once,
but the handle is reused, the stage will only be executed once.

The main takeaway is that you will most likely want to call a stage function only once and reuse
the result as needed.
"""

import foundations
import config
from common.data import load_titanic
from common.prep import require
from common.logging import log_data

load_titanic = foundations.create_stage(load_titanic)
require = foundations.create_stage(require)
log_data = foundations.create_stage(log_data)

def main():
    # redefining the stage twice will not cache the data
    data = 'hello world'
    log = log_data(data)
    log2 = log_data(data)
    executor = require(log, log2)

    # when you do .run(), you deploy a job to run in a (possibly remote) execution environment
    # when you do .run_same_process(), the stage runs in the driver process
    # this is used purely to show that in the execution environment, there is an in-memory cache as described above
    # the user will want to use .run() instead of .run_same_process() essentially 100% of the time
    executor.run_same_process()

    # reusing the same stage will read the data from the in-memory cache
    data = 'bye bye'
    log = log_data(data)
    executor = require(log, log)
    executor.run_same_process()

if __name__ == '__main__':
    main()
