class SSHUtils(object):

    def __init__(self, config):
        self._config = config

    def ssh_arguments(self):
        return '-oBatchMode=yes -i ' + self._key_path()

    def user_at_host(self):
        return self._config['remote_user'] + '@' + self._config['remote_host']

    def command_in_shell_command(self, command):
        return [self._shell_command(), '--login', '-c', command]

    def _shell_command(self):
        return self._config['shell_command']

    def _key_path(self):
        return self._config['key_path']
