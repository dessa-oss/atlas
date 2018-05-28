class ResultReader(object):

    def __init__(self, result_fetcher):
        self.results = result_fetcher.fetch_results()

    def _to_pandas(self):
        import pandas
        return pandas.DataFrame(self.results)

    def _as_dict(self):
        return self.results

    def _as_json(self):
        import json
        return json.dumps(self.results)

    def get_job_information(self):
        import datetime
        import pandas as pd

        all_job_information = []

        main_headers = ["Job ID", "Job Status", "Stage ID", "Parent Stage IDs",
                        "Stage Name", "Args", "Kwargs", "Start Time", "End Time", "Elapsed Time"]

        for job_result in self.results:
            job_id = job_result["config"]["job_name"]
            job_status = None

            try:
                if job_result["error"]:
                    job_status = "failed"
                else:
                    job_status = "succeeded"
            except:
                job_status = "succeeded"

            meta_data = job_result["meta_data"]

            for entry_key, stage_set in job_result["provenance"].iteritems():
                if entry_key != "global":
                    for stage_id, stage_info in stage_set.iteritems():
                        stage_name = stage_info["function_name"]
                        column_headers = list(main_headers)

                        start_time = None
                        end_time = None
                        elapsed_time = None

                        try:
                            meta_data_entry = meta_data[stage_id]

                            start_time = datetime.datetime.fromtimestamp(
                                meta_data_entry["start_time"])
                            end_time = datetime.datetime.fromtimestamp(
                                meta_data_entry["end_time"])
                            elapsed_time = meta_data_entry["delta_time"]
                        except:
                            pass

                        stage_name = stage_info.get("function_name", None)
                        parent_stage_ids = stage_info["parents"]

                        args = []
                        kwargs = {}
                        row_data = [job_id, job_status, stage_id, parent_stage_ids,
                                    stage_name, args, kwargs, start_time, end_time, elapsed_time]

                        for arg in stage_info["args"]:
                            if isinstance(arg, dict):
                                try:
                                    arg_stage_id = arg["stage_id"]
                                    args.append(arg_stage_id)

                                    parent_stage_ids.append(arg_stage_id)
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

                        for arg_name, arg_val in stage_info["kwargs"].iteritems():
                            if isinstance(arg_val, dict):
                                try:
                                    arg_val_stage_id = arg_val["stage_id"]
                                    kwargs.update({arg_name: arg_val_stage_id})

                                    parent_stage_ids.append(arg_val_stage_id)
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

                        all_job_information.append(pd.DataFrame(
                            data=[row_data], columns=column_headers))

        output_dataframe = pd.concat(all_job_information, ignore_index=True)
        fixed_headers = restructure_headers(
            list(output_dataframe), main_headers)
        return output_dataframe[fixed_headers]

    def get_results(self):
        import pandas as pd

        all_job_information = []
        main_headers = ["Job ID", "Stage ID",
                        "Stage Name", "Has Unstructured Result?"]

        for job_result in self.results:
            job_id = job_result["config"]["job_name"]
            persisted_data = job_result["persisted_data"]

            structured_results = job_result["results"]
            stage_ids_with_names = {}

            for entry_key, stage_set in job_result["provenance"].iteritems():
                if entry_key != "global":
                    for stage_id, stage_info in stage_set.iteritems():
                        stage_name = stage_info["function_name"]
                        stage_ids_with_names.update({stage_id: stage_name})

            for stage_id, stage_name in stage_ids_with_names.iteritems():
                column_headers = list(main_headers)
                has_unstructured_result = None

                try:
                    has_unstructured_result = persisted_data[
                        stage_id] is not None
                except:
                    has_unstructured_result = False

                row_data = [job_id, stage_id,
                            stage_name, has_unstructured_result]

                try:
                    for structured_result_name, structured_result_val in structured_results[stage_id].iteritems():
                        column_headers.append(structured_result_name)
                        row_data.append(structured_result_val)
                except:
                    pass

                all_job_information.append(pd.DataFrame(
                    data=[row_data], columns=column_headers))

        output_dataframe = pd.concat(all_job_information, ignore_index=True)
        fixed_headers = restructure_headers(
            list(output_dataframe), main_headers)
        return output_dataframe[fixed_headers]

    def get_unstructured_results(self, stage_ids):
        def get_unstructured_result(stage_id):
            result = None

            for job_result in self.results:
                persisted_data = job_result["persisted_data"]
                try:
                    result = persisted_data[stage_id]
                except:
                    continue

            return result

        return map(get_unstructured_result, stage_ids)
