class SSHUtils(object):

    def __init__(self, config):
        self._config = config

    def ssh_arguments(self):
        return '-oBatchMode=yes -i ' + self._key_path()

    def user_at_host(self):
        return self._config['remote_user'] + '@' + self._config['remote_host']

    def command_in_shell_command(self, command):
        return [self._shell_command(), '--login', '-c', command]

    def command_in_ssh_command(self, command):
        from pipes import quote

        ssh_command = 'ssh ' + self.ssh_arguments() + ' ' + self.user_at_host() + \
            ' ' + quote(command)
        return self.command_in_shell_command(ssh_command)

    def execute_to_remote_scp(self, local_path, remote_path):
        command = self.to_remote_scp_command(local_path, remote_path)
        _, _, code = self.execute_command(command)
        if code != 0:
            raise Exception('Unable to upload {} to {} (code: {})'.format(
                local_path, remote_path, code))

    def to_remote_scp_command(self, local_path, remote_path):
        from pipes import quote
        from os.path import basename

        file_name = basename(local_path)
        ssh_command = 'scp ' + self.ssh_arguments() + ' ' + quote(local_path) + ' ' + \
            quote(self._remote_path(remote_path) + '/' + file_name)
        return self.command_in_shell_command(ssh_command)

    def execute_to_local_scp(self, remote_path, local_path):
        command = self.to_local_scp_command(remote_path, local_path)
        _, _, code = self.execute_command(command)
        if code != 0:
            raise Exception('Unable to download {} to {} (code: {})'.format(
                remote_path, local_path, code))

    def to_local_scp_command(self, remote_path, local_path):
        from pipes import quote
        
        ssh_command = 'scp ' + self.ssh_arguments() + ' ' + \
            quote(self._remote_path(remote_path)) + ' ' + quote(local_path)
        return self.command_in_shell_command(ssh_command)

    def call_command(self, command):
        _, _, status_code = self.execute_command(command)
        return status_code

    def execute_command(self, command):
        from subprocess import PIPE
        from subprocess import Popen

        self._log().debug('Executing command %s', repr(command))

        process = Popen(command, stdout=PIPE, stderr=PIPE)
        result = process.communicate()
        return result[0], result[1], process.returncode

    def _remote_path(self, path):
        return self.user_at_host() + ':' + path

    def _shell_command(self):
        return self._config['shell_command']

    def _key_path(self):
        return self._config['key_path']

    def _log(self):
        from vcat.global_state import log_manager
        return log_manager.get_logger(__name__)
