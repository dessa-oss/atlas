from vcat.stage_piping import StagePiping
from vcat.job import Job
from vcat.successive_argument_filler import SuccessiveArgumentFiller
from vcat.stage_connector import StageConnector
from vcat.stage_smart_constructor import StageSmartConstructor
from vcat.stage_context import StageContext
from vcat.context_aware import ContextAware

class StageConnectorWrapper(object):

    def __init__(self, connector, pipeline_context, stage_context):
        self._connector = connector
        self._pipeline_context = pipeline_context
        self._stage_context = stage_context

        self._stage_context.uuid = self._connector.current_stage.uuid
        self._pipeline_context.add_stage_context(self._stage_context)

        self._stage_piping = StagePiping(self)
        self._persist = False

    def _reset_state(self):
        self._connector._reset_state()

    def tree_names(self, **filler_kwargs):
        all_stages = {}
        self._connector.add_tree_names(
            all_stages, self._provenance_filler_builder, **filler_kwargs)
        return all_stages

    def stage(self, function, *args, **kwargs):
        new_context = StageContext()
        stage_smart_constructor = StageSmartConstructor(new_context)

        if isinstance(function, ContextAware):
            function._set_context(new_context)

        new_stage = stage_smart_constructor.make_stage(new_context, function, *args, **kwargs)
        return StageConnectorWrapper(self._connector.stage(new_stage), self._pipeline_context, new_context)

    def persist(self):
        self._persist = True

    def cache(self, name):
        self._connector.cache(name)

    def __or__(self, stage_args):
        return self._stage_piping.pipe(stage_args)

    def run(self, **filler_kwargs):
        self._pipeline_context.provenance.stage_provenance[
            self._connector.current_stage.uuid] = self.tree_names(**filler_kwargs)
        return self.run_without_provenance(**filler_kwargs)

    def run_without_provenance(self, **filler_kwargs):
        try:
            result = self._connector.run(self._filler_builder, **filler_kwargs)
        except:
            import sys
            self._stage_context.add_error_information(sys.exc_info())
            raise

        if self._persist:
            self._stage_context.stage_output = result

        return result

    def _filler_builder(self, *args, **kwargs):
        from vcat.hyperparameter_argument_fill import HyperparameterArgumentFill
        from vcat.stage_connector_wrapper_fill import StageConnectorWrapperFill

        return SuccessiveArgumentFiller([HyperparameterArgumentFill, StageConnectorWrapperFill], *args, **kwargs)

    def _provenance_filler_builder(self, *args, **kwargs):
        from vcat.hyperparameter_argument_name_fill import HyperparameterArgumentNameFill
        from vcat.stage_connector_wrapper_name_fill import StageConnectorWrapperNameFill

        return SuccessiveArgumentFiller([HyperparameterArgumentNameFill, StageConnectorWrapperNameFill], *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def name(self):
        return self._connector.name()

    def splice(self, num_children):
        def splice_at(data_frames, slot_num):
            return data_frames[slot_num]

        children = []

        for child_index in range(num_children):
            child = self | (splice_at, child_index)
            children.append(child)

        return children
