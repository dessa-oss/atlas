"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat import JobPersister, ResultReader, LocalFileSystemPipelineListing
import config

def main():
    listing = LocalFileSystemPipelineListing(config.archive_root)
    print(listing.get_pipeline_names())

    with JobPersister.load_archiver_fetch() as fetch:
        reader = ResultReader(fetch)
        print(reader.get_results())

if __name__ == '__main__':
    main()
