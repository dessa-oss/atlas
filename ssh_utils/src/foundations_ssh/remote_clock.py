"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

class RemoteClock(object):
    """Used to get the UTC timestamp for current time on a remote machine.
    """

    def __init__(self):
        from foundations_ssh.paramiko_manager import ParamikoManager

        self._paramiko = ParamikoManager()       

    def time(self):
        with self._paramiko as client:
            timestamp_string = self._paramiko.exec_command("date +%s")
        
        return int(timestamp_string)