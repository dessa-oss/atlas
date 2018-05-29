from vcat.stage_piping import StagePiping
from vcat.job import Job
from vcat.successive_argument_filler import SuccessiveArgumentFiller
from vcat.stage_connector import StageConnector
from vcat.stage_smart_constructor import StageSmartConstructor
from vcat.stage_context import StageContext


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
        new_stage = stage_smart_constructor.make_stage(self._stage_context, function, *args, **kwargs)
        return StageConnectorWrapper(self._connector.stage(new_stage), self._pipeline_context, new_context)

    def persist(self):
        self._persist = True

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

    def _grid_param_set_generator(self, dict_of_hyper_params):
        import itertools

        param_keys = []
        param_vals_to_select = []

        for key, val in dict_of_hyper_params.iteritems():
            param_keys.append(key)
            param_vals_to_select.append(val)

        for param_vals in itertools.product(*param_vals_to_select):
            param_set_entry = {}

            for param_key, param_val in zip(param_keys, param_vals):
                param_set_entry[param_key] = param_val

            yield param_set_entry

    def grid_search(self, deployer_type, **hype_kwargs):
        import time
        import uuid

        hype_dict = {}

        for key, val in hype_kwargs.iteritems():
            if isinstance(val, list):
                hype_dict[key] = val
            else:
                hype_dict[key] = [val]

        for param_set in self._grid_param_set_generator(hype_dict):
            self._reset_state()
            job = Job(self, **param_set)
            deployer = deployer_type(str(uuid.uuid4()), job)

            deployer.deploy()

            while not deployer.is_job_complete():
                print "Waiting for job \"" + deployer.job_name() + "\" to finish..."
                time.sleep(5)

            print "Fetching results..."
            # results_dict = deployer.fetch_job_results()

            print "Job \"" + deployer.job_name() + "\" has completed."

    def adaptive_search(self, deployer_type, initial_generator, generator_function):
        def extract_results(results_dict):
            results = {}

            for result_entry in results_dict["results"].values():
                results.update(result_entry)

            return results

        import Queue
        import time
        import uuid

        queue = Queue.Queue()

        for initial_params in initial_generator:
            queue.put(initial_params)

        while not queue.empty():
            self._reset_state()

            param_set = queue.get()
            job = Job(self, **param_set)
            deployer = deployer_type(str(uuid.uuid4()), job)
            deployer.deploy()

            while not deployer.is_job_complete():
                print "Waiting for job \"" + deployer.job_name() + "\" to finish..."
                time.sleep(5)

            print "Fetching results..."
            results_dict = deployer.fetch_job_results()

            print "Job \"" + deployer.job_name() + "\" has completed."

            for new_params in generator_function(extract_results(results_dict)):
                queue.put(new_params)

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
