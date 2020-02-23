
class JobSourceBundle(object):

    def __init__(self, bundle_name, target_path):
        self._bundle_name = bundle_name
        self._path = target_path

    @staticmethod
    def from_dict(job_source_bundle_dict):
        return JobSourceBundle(job_source_bundle_dict['bundle_name'], job_source_bundle_dict['target_path'])

    @staticmethod
    def for_deployment():
        from uuid import uuid4
        from tempfile import mkdtemp

        bundle_name = str(uuid4())
        return JobSourceBundle(bundle_name, mkdtemp() + '/')

    def bundle(self):
        import tarfile
        import os

        self._log().info('Preparing to bundle contents of {} for execution. Estimating bundle size.'.format(os.getcwd()))
        size = self._get_size(os.getcwd())
        for i in [500, 100, 50]:
            if size/1024./1024. > i:
                self._log().warn('Directory size is larger than {}MB!'.format(i))
                self._log().warn('Please ensure you have the right job directory specified. If you have large artifacts in')
                self._log().warn('your job directory, you can use other methods to retrieve artifacts during your job run')
                self._log().warn('to avoid performance issues. Please see documentation for details.')
                self._log().warn('Ctr-C to cancel the bundling and job submission process')
                break
        self._log().info('Bundling job contents.')
        with tarfile.open(self.job_archive(), "w:gz") as tar:
            tar.add(".")
            for item in tar:
                self._log().debug('Added %s to source bundle', item.name)

    def unbundle(self, path_to_save):
        import tarfile
        from distutils.dir_util import mkpath
        from foundations_internal.change_directory import ChangeDirectory

        with tarfile.open(self.job_archive(), "r:gz") as tar:
            mkpath(path_to_save)
            with ChangeDirectory(path_to_save):
                tar.extractall()

    def cleanup(self):
        from os import remove
        from os.path import exists

        if exists(self.job_archive()):
            remove(self.job_archive())

    def job_archive_name(self):
        return self._bundle_name + ".tgz"

    def job_archive(self):
        return self._path + self.job_archive_name()

    def file_listing(self):
        import tarfile

        with tarfile.open(self.job_archive(), "r:gz") as tar:
            for tarinfo in tar:
                yield tarinfo.name

    def _log(self):
        from foundations_contrib.global_state import log_manager
        return log_manager.get_logger(__name__)

    def _get_size(self, start_path):
        import os
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        return total_size