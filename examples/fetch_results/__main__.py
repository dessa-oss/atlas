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

See comments below for a walkthrough.
"""

# import utilities that aid in deserialization as well as reading from the file system,
# and the result reader itself
from foundations import JobPersister, ResultReader, log_manager


def main():
    # get a logger - like using print, but more configurable
    log = log_manager.get_logger(__name__)

    # create a lookup object (already configured to read from local filesystem)
    with JobPersister.load_archiver_fetch() as fetch:

        # create a result reader from the lookup object
        reader = ResultReader(fetch)

        # get and print results
        log.info("\n{}".format(reader.get_results()))

if __name__ == '__main__':
    main()
