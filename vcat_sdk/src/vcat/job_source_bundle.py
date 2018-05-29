class JobSourceBundle(object):

    def __init__(self, bundle_name, target_path):
        self._bundle_name = bundle_name
        self._path = target_path

    def bundle(self):
        import tarfile

        with tarfile.open(self.job_archive(), "w:gz") as tar:
            tar.add(".")

    def unbundle(self):
        import tarfile

        with tarfile.open(self.job_archive(), "r:gz") as tar:
            tar.extractall()

    def cleanup(self):
        import os
        os.remove(self.job_archive())

    def job_archive_name(self):
        return self._bundle_name + ".tgz"

    def job_archive(self):
        return self._path + self.job_archive_name()

    def file_listing(self):
        import tarfile

        with tarfile.open(self.job_archive(), "r:gz") as tar:
            for tarinfo in tar:
                yield tarinfo.name
        