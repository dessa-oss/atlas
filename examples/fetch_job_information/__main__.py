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
information for all jobs that have stored their results in an accessible location (e.g.
S3, GS, local directory).  In this example, we query job information stored on the
local filesystem and return them into a dataframe - this allows for sorting, filtering,
and so forth.

As a walkthrough (line numbers given):
    27: import utilities that aid in deserialization as well reading from the file system,
        and the result reader itself
    31: get a logger - like using print, but more configurable
    32: create an adapter to read from the local filesystem
    34: create a lookup object for use with the filesystem adapter
    35: create a result reader from the lookup object
    36: get and print job information
"""

from foundations import JobPersister, ResultReader, LocalFileSystemPipelineListing, log_manager
import config

def main():
    log = log_manager.get_logger(__name__)
    # listing = LocalFileSystemPipelineListing(config.archive_root)

    with JobPersister.load_archiver_fetch() as fetch:
        reader = ResultReader(fetch)
        log.info("\n{}".format(reader.get_job_information()))

if __name__ == '__main__':
    main()
