from vcat_ssh.ssh_utils import SSHUtils


class SSHListing(object):

    def __init__(self):
        from vcat.global_state import config_manager
        self._config = config_manager.config()
        self._ssh_utils = SSHUtils(self._config)

    def track_pipeline(self, pipeline_name):
        pass

    def get_pipeline_names(self):
        archives = self._list_archive_names()
        return [self._archive_without_extension(archive_name) for archive_name in archives]

    def _archive_without_extension(self, archive):
        return archive[0:-4]

    def _list_archive_names(self):
        from os.path import basename

        archives = self._list_archives()
        return [basename(path) for path in archives]

    def _list_archives(self):
        from subprocess import Popen
        from subprocess import PIPE

        command = self._list_archives_command()
        process = Popen(command, stdout=PIPE)
        stdout, _ = process.communicate()
        return stdout.strip().split("\n")

    def _list_archives_command(self):
        ssh_command = 'ssh ' + self._ssh_utils.ssh_arguments() + ' ' + self._ssh_utils.user_at_host() + ' "ls -1 ' + \
            self._result_path() + '/*.tgz' + '"'
        return self._ssh_utils.command_in_shell_command(ssh_command)

    def _result_path(self):
        return self._config['result_path']
