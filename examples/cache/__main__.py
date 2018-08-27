"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
Please have a look at and understand the local_cache module before looking at this one -
it is similar to this one but there is a key, subtle difference.

This concept of caching is more of a global one.  If you expect that your job
has stages in common with another job you've previously run, and that the output
data should be the same for those stages, why not just use the results from the
previous job?  If you call .enable_caching() on a stage, this is exactly what will
happen.  If the stage has not been run before, it will run the stage and store the
result in a configurable location (e.g. S3, local filesystem).  If the stage is run
a second time within a different job, its result will be recalled and used.

The cache location is set in a configuration yaml provided as result of integration /
installation of Foundations.  It can also be set programmatically - see the config
module for an example of how to do this.  

Contrast this with the caching described in local_cache; the cache there exists for the
lifetime of the job.  It is always enabled and exists in memory.  The cache here
exists across jobs and exists on a filesystem-like storage.  It must be called manually.
"""

import foundations
import config
from common.data import load_titanic
from common.prep import require
from common.logging import log_data

load_titanic = foundations.create_stage(load_titanic)
require = foundations.create_stage(load_titanic)
log_data = foundations.create_stage(log_data)


def main():
    # we have two stages log, and log2
    # since they are derived from the same code ("log_data"),
    # there'd be no point in actually executing both

    data = 'hello world'
    log = log_data(data)

    # mark the stage ("log") as cacheable
    # this means its result will be:
    #     1. looked up in cache
    #     2a. if success, the result will be returned without further computation
    #     2b. if failure, the result will be computed and saved to cache
    log.enable_caching()

    log2 = log_data(data)

    # see previous comment - since log2 is derived from the same code as log,
    # its result should be successfully looked up from the cache - log2 should not actually be executed
    # (assuming the log2 stage executes after log)
    log2.enable_caching()
    
    executor = require(log, log2)
    executor.run_same_process()

if __name__ == '__main__':
    main()
