"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ResultReader(object):

    def __init__(self, pipeline_archiver_fetch):
        from foundations.pipeline_context import PipelineContext
        from foundations.job_source_bundle import JobSourceBundle

        self._pipeline_contexts = {}
        self._archivers = {}

        for pipeline_archiver in pipeline_archiver_fetch.fetch_archivers():
            pipeline_context = PipelineContext()
            pipeline_context.file_name = pipeline_archiver.pipeline_name()
            pipeline_context.provenance.job_source_bundle = JobSourceBundle(pipeline_context.file_name, "./")
            self._archivers[pipeline_context.file_name] = pipeline_archiver

            self._pipeline_contexts[pipeline_archiver.pipeline_name()] = pipeline_context

    def cleanup(self):
        for pipeline_context in self._pipeline_contexts.values():
            pipeline_context.provenance.job_source_bundle.cleanup()

    @staticmethod
    def _fill_placeholders(provenance, params_to_read, params_to_write, parent_ids, column_headers, row_data):
        from foundations.utils import dict_like_iter, dict_like_append

        for arg_name, argument_value in dict_like_iter(params_to_read):
            argument_name = argument_value['name']
            argument_value = argument_value['value']
            if argument_value['type'] == 'stage':
                argument_value_stage_uuid = argument_value["stage_uuid"]
                dict_like_append(params_to_write, arg_name, argument_value_stage_uuid)

                parent_ids.append(argument_value_stage_uuid)
            elif argument_value['type'] == 'dynamic':
                hyperparameter_name = argument_name
                hyperparameter_value = provenance.job_run_data.get(
                    argument_value['name'])

                if hyperparameter_name:
                    dict_like_append(params_to_write, arg_name, hyperparameter_name)

                    column_headers.append(
                        hyperparameter_name)
                    row_data.append(hyperparameter_value)
                else:
                    dict_like_append(params_to_write, arg_name, hyperparameter_value)
            else:
                dict_like_append(params_to_write, arg_name, argument_value)

    @staticmethod
    def _create_initial_row_data(args, kwargs, stage_context, stage_info, stage_id, pipeline_name):
        from foundations.utils import pretty_time

        parent_ids = stage_info.parents
        stage_name = stage_info.function_name

        start_time = pretty_time(stage_context.start_time)
        end_time = pretty_time(stage_context.end_time)
        delta_time = stage_context.delta_time

        if stage_context.error_information:
            stage_status = "failed"
        else:
            stage_status = "succeeded"

        return [pipeline_name, stage_status, stage_id, parent_ids, stage_name,
            args, kwargs, start_time, end_time, delta_time]

    @staticmethod
    def _add_stage_results(all_job_information, stage_hierarchy_entries, pipeline_name, pipeline_context, main_headers):
        import pandas as pd

        for stage_id, stage_info in stage_hierarchy_entries.items():
            column_headers = list(main_headers)

            stage_name = stage_info.function_name
            stage_context = pipeline_context.stage_contexts[stage_id]

            has_unstructured_result = stage_context.has_stage_output

            row_data = [pipeline_name, stage_id, stage_name, has_unstructured_result]

            if stage_context.has_stage_output or len(stage_context.stage_log) > 0:
                for log_item in stage_context.stage_log:
                    structured_result_name = log_item['key']
                    structured_result_val = log_item['value']
                    column_headers.append(structured_result_name)
                    row_data.append(structured_result_val)

                all_job_information.append(pd.DataFrame(data=[row_data], columns=column_headers))

    @staticmethod
    def _create_frame_with_ordered_headers(main_headers, callback):
        import pandas as pd

        from foundations.utils import restructure_headers

        all_job_information = [pd.DataFrame(columns=main_headers)]

        callback(main_headers, all_job_information)

        output_dataframe = pd.concat(all_job_information, ignore_index=True)
        fixed_headers = restructure_headers(list(output_dataframe), main_headers)
        return output_dataframe[fixed_headers]

    def _load_job_provenance(self, pipeline_context, pipeline_name):
        pipeline_context.load_provenance_from_archive(self._archivers[pipeline_name])

    def _get_results(self, main_headers, all_job_information):
        for pipeline_name, pipeline_context in self._pipeline_contexts.items():
            self._load_job_provenance(pipeline_context, pipeline_name)
            pipeline_context.load_stage_log_from_archive(self._archivers[pipeline_name])

            stage_hierarchy_entries = pipeline_context.provenance.stage_hierarchy.entries

            ResultReader._add_stage_results(
                all_job_information, stage_hierarchy_entries, pipeline_name, pipeline_context, main_headers)

    def get_results(self):
        main_headers = ["job_name", "stage_id",
                        "stage_name", "has_unstructured_result"]

        return ResultReader._create_frame_with_ordered_headers(main_headers, self._get_results)

    def _get_job_information(self, main_headers, all_job_information):
        import pandas as pd

        for pipeline_name, pipeline_context in self._pipeline_contexts.items():
            self._load_job_provenance(pipeline_context, pipeline_name)
            stage_hierarchy_entries = pipeline_context.provenance.stage_hierarchy.entries

            for stage_id, stage_info in stage_hierarchy_entries.items():
                self._log().debug('Loading job information for %s at stage %s', repr(pipeline_name), repr(stage_id))

                column_headers = list(main_headers)
                stage_context = pipeline_context.stage_contexts[stage_id]

                args = []
                kwargs = []

                row_data = ResultReader._create_initial_row_data(
                    args, kwargs, stage_context, stage_info, stage_id, pipeline_name)

                ResultReader._fill_placeholders(
                    pipeline_context.provenance,
                    stage_info.stage_args, 
                    args, 
                    stage_info.parents, 
                    column_headers, 
                    row_data
                )
                ResultReader._fill_placeholders(
                    pipeline_context.provenance,
                    stage_info.stage_kwargs, 
                    kwargs, 
                    stage_info.parents, 
                    column_headers, 
                    row_data
                )

                all_job_information.append(pd.DataFrame(data=[row_data], columns=column_headers))

    def get_job_information(self):
        main_headers = ["job_name", "stage_status", "stage_id", "parent_ids",
            "stage_name", "args", "kwargs", "start_time", "end_time", "delta_time"]

        return ResultReader._create_frame_with_ordered_headers(main_headers, self._get_job_information)

    def _over_pipeline_contexts(self, callback):
        for pipeline_context in self._pipeline_contexts.values():
            try:
                return callback(pipeline_context)
            except:
                continue
        
        return None

    def _get_unstructured_result(self, pipeline_name):
        def _with_pipeline_id(stage_id):
            pipeline_context = self._pipeline_contexts[pipeline_name]
            pipeline_context.load_persisted_data_from_archive(self._archivers[pipeline_name])
            
            return pipeline_context.stage_contexts[stage_id].stage_output
            
        return _with_pipeline_id

    def get_unstructured_results(self, pipeline_name, stage_ids):
        return map(self._get_unstructured_result(pipeline_name), stage_ids)

    def get_source_code(self, stage_id):
        def _try_get_source_code(pipeline_context):
            pipeline_name = pipeline_context.file_name
            self._load_job_provenance(pipeline_context, pipeline_name)
            return pipeline_context.provenance.stage_hierarchy.entries[stage_id].function_source_code
            
        return self._over_pipeline_contexts(_try_get_source_code)

    def get_error_information(self, pipeline_id, stage_id=None, verbose=False):
        from foundations.utils import pretty_error

        pipeline_context = self._pipeline_contexts[pipeline_id]

        if stage_id is None:
            error_info = pipeline_context.global_stage_context.error_information
        else:
            error_info = pipeline_context.stage_contexts[stage_id].error_information

        return pretty_error(pipeline_id, error_info, verbose=verbose)

    def create_working_copy(self, pipeline_name, path_to_save):
        pipeline_context = self._pipeline_contexts[pipeline_name]
        pipeline_context.load_job_source_from_archive(self._archivers[pipeline_name])
        job_source_bundle = self._pipeline_contexts[pipeline_name].provenance.job_source_bundle
        job_source_bundle.unbundle(path_to_save)

    @staticmethod
    def _static_log():
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__)

    def _log(self):
        return ResultReader._static_log()