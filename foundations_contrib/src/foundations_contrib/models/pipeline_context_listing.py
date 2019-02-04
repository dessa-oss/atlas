"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class PipelineContextListing(object):

    @staticmethod
    def pipeline_contexts():
        for archiver in PipelineContextListing._archivers():
            yield archiver.pipeline_name(), PipelineContextListing._wrapped_context(archiver)

    @staticmethod
    def _wrapped_context(archiver):
        from foundations_contrib.models.pipeline_context_with_archive import PipelineContextWithArchive
        return PipelineContextWithArchive(archiver)

    @staticmethod
    def _archivers():
        from foundations.job_persister import JobPersister

        with JobPersister.load_archiver_fetch() as fetch:
            for archiver in fetch.fetch_archivers():
                yield archiver
