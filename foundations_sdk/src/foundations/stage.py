"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class Stage(object):

    def __init__(self, middleware, uuid, function, metadata_function, *args, **kwargs):
        self._middleware = middleware
        self._uuid = uuid
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self._metadata_function = metadata_function

    def uuid(self):
        return self._uuid

    def run(self, upstream_result_callback, filler_builder, **filler_kwargs):
        def execute(args, kwargs):
            result = self.function(*args, **kwargs)
            self._log().debug('Stage result: %s', repr(result))
            return result
        return self._middleware.call(upstream_result_callback, filler_builder, filler_kwargs, self.args, self.kwargs, execute)

    def filler(self, filler_builder):
        return filler_builder(*self.args, **self.kwargs)

    def fill_args_and_kwargs(self, filler_builder, **filler_kwargs):
        return self.filler(filler_builder).fill(**filler_kwargs)

    def name(self):
        return str(self.uuid())

    def function_name(self):
        return self._metadata_function.__name__

    def function_source_code(self):
        import foundations.safe_inspect as inspect
        return inspect.getsource(self._metadata_function)

    def source_file(self):
        import foundations.safe_inspect as inspect
        return inspect.getsourcefile(self._metadata_function)

    def source_line(self):
        import foundations.safe_inspect as inspect
        return inspect.getsourcelines(self._metadata_function)[1]

    def stage_args(self):
        return self.args

    def stage_kwargs(self):
        return self.kwargs

    def _log(self):
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__)
