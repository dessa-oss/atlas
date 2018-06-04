from vcat_ssh.ssh_utils import SSHUtils


class SSHListing(object):

    def __init__(self):
        from vcat.global_state import config_manager
        self._ssh_utils = SSHUtils(config_manager.config())

    def track_pipeline(self, pipeline_name):
        pass

    def get_pipeline_names(self):
        pass
