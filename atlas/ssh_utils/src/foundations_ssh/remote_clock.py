
class RemoteClock(object):
    """Used to get the UTC timestamp for current time on a remote machine.
    """

    def __init__(self):
        from foundations_ssh.paramiko_manager import ParamikoManager

        self._paramiko = ParamikoManager()       

    def time(self):
        """Get the UTC timestamp for current time on the remote machine as configured by the paramiko manager.

        Returns:
            timestamp -- Integer timestamp for current time on remote machine (UTC)
        """

        with self._paramiko as client:
            timestamp_string = self._paramiko.exec_command("date +%s")
        
        return int(timestamp_string)