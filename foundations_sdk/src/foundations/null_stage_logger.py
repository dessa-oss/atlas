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
        """Not implemented

        Arguments:
            key {string}
            value {object}

        Raises:
            NotImplementedError
        """

        raise NotImplementedError()

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
