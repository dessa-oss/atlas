"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
After you've run your jobs, you'll probably want to see some job metadata, such as
how long the job took to run, as well as which stages fed into other stages of interest.
That's where the ResultReader class comes into play.  It allows you to grab this
information for all jobs that have stored their information in an accessible location (e.g.
S3, GS, local directory).  In this example, we query job information stored on the
local filesystem and return them into a dataframe - this allows for sorting, filtering,
and so forth.

See comments below for a walkthrough.
"""

# import utilities that aid in deserialization as well as reading from the file system,
# and the result reader itself
from foundations import JobPersister, ResultReader, log_manager, config_manager

# set configuration for running the job 
config_manager.add_config_path('config/local_default.config.yaml')

def main():
    # get a logger - like using print, but more configurable
    log = log_manager.get_logger(__name__)

    # create a lookup object (already configured to read from local filesystem)
    with JobPersister.load_archiver_fetch() as fetch:

        # create a result reader from the lookup object
        reader = ResultReader(fetch)

        # get and print job information
        log.info("\n{}".format(reader.get_job_information()))

if __name__ == '__main__':
    main()
