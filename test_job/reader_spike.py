import cProfile
from vcat import *


def run_it(archive_listing, archive):
    with JobPersister.load_archiver_fetch() as pipeline_archiver_fetch:
        return ResultReader(pipeline_archiver_fetch)

reader = run_it(GCPPipelineArchiveListing(), GCPPipelineArchive())
