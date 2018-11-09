"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class StageLogMiddleware(object):
    """
    Middleware class to log metrics from output
    """

    def __init__(self, stage_context):
        self._stage_context = stage_context

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        """
        The call method runs a callback function and logs the result metrics. Metrics are logged with 
        the StageLogger and logged events are also pushed to a message route named 'stage_log_middleware'

        Arguments:
            upstream_result_callback - not used
            filler_builder - not used
            filler_kwargs - not used
            args - arguments for callback function
            kwargs - keyword arguments for callback function
            callback - function to run stage
        
        Return:
            return_value - result from callback execution
        """
        from foundations.stage_logger import StageLogger
        from foundations.global_state import message_router

        stage_output = callback(args, kwargs)
        if isinstance(stage_output, tuple) and len(stage_output) == 2:
            logger = StageLogger(None, None, None, self._stage_context)
            return_value, result = stage_output
            for key, value in result.items():
                message_router.push_message({'key': key, 'value': value}, 'stage_log_middleware')
                logger.log_metric(key, value)              
        else:
            return_value = stage_output
        return return_value
