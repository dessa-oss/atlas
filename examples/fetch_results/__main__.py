"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
After you've run your jobs, you'll probably want to see what the results are.
That's where the ResultReader class comes into play.  It allows you to grab results
for all jobs that have stored their results in an accessible location (e.g. S3, GS,
local directory).  In this example, we query results stored on the local filesystem
and return them into a dataframe - this allows for sorting, filtering, and so forth.

Note: a result is defined as something explicitly logged into a dict during execution
of a stage; see "get_metrics()" in titanic/etl.py for an example.

As a walkthrough (line numbers given):
    28: import utilities that aid in deserialization as well reading from the file system,
        and the result reader itself
    29: configure Foundations to read from the local filesystem - don't worry about this line
    32: get a logger - like using print, but more configurable
    33: create a lookup object (already configured to read from local filesystem)
    34: create a result reader from the lookup object
    35: get and print results
"""

from foundations import JobPersister, ResultReader, log_manager
import config

def main():
    log = log_manager.get_logger(__name__)

    with JobPersister.load_archiver_fetch() as fetch:
        reader = ResultReader(fetch)
        log.info("\n{}".format(reader.get_results()))

if __name__ == '__main__':
    main()
