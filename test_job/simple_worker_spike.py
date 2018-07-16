from foundations import *

bucket = LocalFileSystemBucket('./')
print(bucket.list_files('*'))

SimpleWorker('../tmp/code', '../tmp/results').run()