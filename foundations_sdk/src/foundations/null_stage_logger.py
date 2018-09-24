"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class NullStageLogger(object):
    """
    Dummy implementation of stage logger that will raise error if used
    """

    def log_metric(self, key, value):
        """Does nothing effectively, but provides warning upon 
        useage to encourage a user to use #log_metric within a stage

        Arguments:
            key {str} -- Name of the metric
            value {object} -- Unused
        """

        self._log().warn('Tried to save metric `{}` outside the context of a stage'.format(key))

    def pipeline_context(self):
        """Not implemented

        Raises:
            NotImplementedError
        """

        raise NotImplementedError()

    def stage(self):
        """Not implemented

        Raises:
            NotImplementedError
        """

        raise NotImplementedError()

    def stage_config(self):
        """Not implemented

        Raises:
            NotImplementedError
        """

        raise NotImplementedError()

    def stage_context(self):
        """Not implemented

        Raises:
            NotImplementedError
        """

        raise NotImplementedError()

    def _log(self):
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__)
