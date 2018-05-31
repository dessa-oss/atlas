class ResultReader(object):

    def __init__(self, archive_listing, archive):
        from vcat.pipeline_context import PipelineContext
        from vcat.pipeline_archiver_fetch import PipelineArchiverFetch
        from vcat.job_source_bundle import JobSourceBundle

        self._pipeline_contexts = {}

        with archive as archive_handle:
            pipeline_archiver_fetch = PipelineArchiverFetch(archive_listing, archive_handle,
                archive_handle, archive_handle, archive_handle, archive_handle, archive_handle)
            
        for pipeline_archiver in pipeline_archiver_fetch.fetch_archivers():
            pipeline_context = PipelineContext()
            pipeline_context.provenance.job_source_bundle = JobSourceBundle(pipeline_archiver.pipeline_name(), "./")
            pipeline_context.load_from_archive(pipeline_archiver)

            self._pipeline_contexts[pipeline_archiver.pipeline_name()] = pipeline_context

    def cleanup(self):
        for pipeline_context in self._pipeline_contexts.values():
            pipeline_context.provenance.job_source_bundle.cleanup()

    def _pretty_time(self, timestamp):
        import datetime

        try:
            return datetime.datetime.fromtimestamp(timestamp)
        except:
            return timestamp

    def get_job_information(self):
        import datetime
        import pandas as pd

        from vcat import restructure_headers

        all_job_information = []

        main_headers = ["pipeline_name", "stage_status", "stage_id", "parent_ids",
            "stage_name", "args", "kwargs", "start_time", "end_time", "delta_time"]

        for pipeline_name, pipeline_context in self._pipeline_contexts.iteritems():
            stage_hierarchy_entries = pipeline_context.provenance.stage_hierarchy.entries

            for stage_id, stage_info in stage_hierarchy_entries.iteritems():
                column_headers = list(main_headers)

                parent_ids = stage_info.parents
                stage_name = stage_info.function_name
                args = []
                kwargs = []

                stage_context = pipeline_context.stage_contexts[stage_id]

                start_time = self._pretty_time(stage_context.start_time)
                end_time = self._pretty_time(stage_context.end_time)
                delta_time = stage_context.delta_time

                if stage_context.error_information:
                    stage_status = "failed"
                else:
                    stage_status = "succeeded"

                row_data = [pipeline_name, stage_status, stage_id, parent_ids, stage_name,
                    args, kwargs, start_time, end_time, delta_time]

                for arg in stage_info.stage_args:
                    if isinstance(arg, dict):
                        try:
                            arg_stage_id = arg["stage_id"]
                            args.append(arg_stage_id)

                            parent_ids.append(arg_stage_id)
                        except:
                            hyperparameter_name = arg.get(
                                "hyperparameter_name", None)
                            hyperparameter_value = arg[
                                "hyperparameter_value"]

                            if hyperparameter_name:
                                args.append(hyperparameter_name)

                                column_headers.append(
                                    hyperparameter_name)
                                row_data.append(hyperparameter_value)
                            else:
                                args.append(hyperparameter_value)
                    else:
                        args.append(arg)

                for arg_name, arg_val in stage_info.stage_kwargs.iteritems():
                    if isinstance(arg_val, dict):
                        try:
                            arg_val_stage_id = arg_val["stage_id"]
                            kwargs.update({arg_name: arg_val_stage_id})

                            parent_ids.append(arg_val_stage_id)
                        except:
                            hyperparameter_name = arg_val.get(
                                "hyperparameter_name", None)
                            hyperparameter_value = arg_val[
                                "hyperparameter_value"]

                            if hyperparameter_name:
                                kwargs.update(
                                    {arg_name: hyperparameter_name})

                                column_headers.append(
                                    hyperparameter_name)
                                row_data.append(hyperparameter_value)
                            else:
                                kwargs.append(
                                    {arg_name: hyperparameter_value})
                    else:
                        kwargs.update({arg_name: arg_val})

                all_job_information.append(pd.DataFrame(data=[row_data], columns=column_headers))
    
        output_dataframe = pd.concat(all_job_information, ignore_index=True, sort=False)
        fixed_headers = restructure_headers(list(output_dataframe), main_headers)
        return output_dataframe[fixed_headers]

    def get_results(self):
        import pandas as pd

        from vcat import restructure_headers

        all_job_information = []
        main_headers = ["pipeline_name", "stage_id",
                        "stage_name", "has_unstructured_result"]

        for pipeline_name, pipeline_context in self._pipeline_contexts.iteritems():
            stage_hierarchy_entries = pipeline_context.provenance.stage_hierarchy.entries

            for stage_id, stage_info in stage_hierarchy_entries.iteritems():
                column_headers = list(main_headers)

                stage_name = stage_info.function_name
                stage_context = pipeline_context.stage_contexts[stage_id]

                has_unstructured_result = stage_context.stage_output is not None

                row_data = [pipeline_name, stage_id, stage_name, has_unstructured_result]

                for structured_result_name, structured_result_val in stage_context.stage_log.iteritems():
                    column_headers.append(structured_result_name)
                    row_data.append(structured_result_val)

                all_job_information.append(pd.DataFrame(data=[row_data], columns=column_headers))

        output_dataframe = pd.concat(all_job_information, ignore_index=True, sort=False)
        fixed_headers = restructure_headers(list(output_dataframe), main_headers)
        return output_dataframe[fixed_headers]

    def get_unstructured_results(self, stage_ids):
        def get_unstructured_result(stage_id):
            for pipeline_context in self._pipeline_contexts.values():
                try:
                    return pipeline_context.stage_contexts[stage_id].stage_output
                except:
                    continue

            return None

        return map(get_unstructured_result, stage_ids)

    def get_source_code(self, stage_id):
        for pipeline_context in self._pipeline_contexts.values():
            try:
                return pipeline_context.provenance.stage_hierarchy.entries[stage_id].function_source_code
            except:
                continue
        return None