from vcat.stage import Stage
from vcat.utils import merged_uuids
from vcat.argument_hasher import ArgumentHasher


class StageSmartConstructor(object):

    def __init__(self, stage_context):
        self._stage_context = stage_context

    def make_stage(self, current_uuid, stage_context, function, *args, **kwargs):
        stage_uuid = self._make_uuid(current_uuid, function, args, kwargs)
        stage_context.uuid = stage_uuid
        return Stage(stage_uuid, self._wrapped_function(stage_uuid, function), function, *args, **kwargs)

    def _make_uuid(self, current_uuid, function, args, kwargs):
        argument_hasher = ArgumentHasher(args, kwargs)
        argument_uuid = argument_hasher.make_hash()
        function_uuid = self._function_hash(function)
        return merged_uuids([current_uuid, function_uuid, argument_uuid])

    def _function_hash(self, function):
        from vcat.utils import generate_uuid
        from vcat.utils import merged_uuids
        from vcat.safe_inspect import *

        name_uuid = generate_uuid(function.__name__)
        source_uuid = generate_uuid(getsource(function))

        return merged_uuids([name_uuid, source_uuid])

    def _wrapped_function(self, stage_uuid, function):
        def wrapped(*args, **kwargs):
            def callback():
                stage_output = function(*args, **kwargs)
                if isinstance(stage_output, tuple):
                    return_value, result = stage_output
                    self._stage_context.stage_log = result
                else:
                    return_value = stage_output
                return return_value
            return self._stage_context.time_callback(callback)
        return wrapped
