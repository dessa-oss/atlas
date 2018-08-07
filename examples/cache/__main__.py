"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
Please have a look at and understand the local_cache module before looking at this one -
it is similar to this one but there is a key, subtle similarity.

This concept of caching is more of a global one.  If you expect that your job
has stages in common with another job you've previously run, and that the output
data should be the same for those stages, why not just use the results from the
previous job?  If you call .enable_caching() on a stage, this is exactly what will
happen.  If the stage has not been run before, it will run the stage and store the
result in a configurable location (e.g. S3, local filesystem).  If the stage is run
a second time within a different job, its result will be recalled and used.

Contrast this with the caching described in local_cache; the cache there exists for the
lifetime of the job.  It is always enabled and exists in memory.  The cache here
exists across jobs and exists on a filesystem-like storage.  It must be called manually.
"""

import foundations
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