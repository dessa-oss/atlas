class ArgumentHasher(object):

    def __init__(self, args, kwargs):
        self._args = args
        self._kwargs = kwargs

    def make_hash(self):
        from vcat.utils import merged_uuids

        return merged_uuids(self._arg_hashes() + self._kwarg_hashes())

    def _arg_hashes(self):
        return [self._make_argument_hash(arg) for arg in self._args]

    def _kwarg_hashes(self):
        from vcat.utils import generate_uuid

        results = []
        for key, value in self._kwargs.items():
            results.append(generate_uuid(key))
            results.append(self._make_argument_hash(value))

    def _make_argument_hash(self, item):
        from vcat.utils import generate_uuid
        from vcat.pipeline import Pipeline
        from vcat.stage_connector_wrapper import StageConnectorWrapper
        from vcat.hyperparameter import Hyperparameter

        if isinstance(item, basestring):
            return generate_uuid(item)

        if isinstance(item, Pipeline) or isinstance(item, StageConnectorWrapper) or isinstance(item, Pipeline):
            return item.uuid()

        if isinstance(item, Hyperparameter):
            return generate_uuid(item.name)

        return generate_uuid(str(item))
