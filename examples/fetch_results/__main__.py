"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations import JobPersister, ResultReader, LocalFileSystemPipelineListing, log_manager
import config

def main():
    log = log_manager.get_logger(__name__)
    listing = LocalFileSystemPipelineListing(config.archive_root)

    with JobPersister.load_archiver_fetch() as fetch:
        reader = ResultReader(fetch)
        log.info("\n{}".format(reader.get_results()))

if __name__ == '__main__':
    main()
