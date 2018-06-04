from vcat import *

config_manager.ensure_logging_configured()
bucket = LocalFileSystemBucket('./')
print(bucket.list_files('*'))

SimpleWorker('../tmp/code', '../tmp/results').run()