class GCPBundleFetcher(object):

    def __init__(self):
        from google.cloud.storage import Client
        from googleapiclient import discovery

        self._gcp_bucket_connection = Client()
        self._result_bucket_connection = self._gcp_bucket_connection.get_bucket(
            'tango-result-test')

    def fetch_results(self):
        import os
        import dill as pickle
        import tarfile
        import shutil

        objects = self._result_bucket_connection.list_blobs(
            prefix="bundled_contexts/")
        results = []
        for result_object in objects:
            file_name = os.path.basename(result_object.name)
            with open(file_name, "w+b") as file:
                result_object.download_to_file(file)
            directory_name = os.path.splitext(file_name)[0]
            with tarfile.open(file_name, "r:gz") as tar:
                tar.extractall()
            with open(directory_name + "/context.pkl", "rb") as file:
                context = pickle.load(file)

            persisted_data = context["persisted_data"]
            for key, value in persisted_data.items():
                with open(directory_name + "/" + value, "rb") as file:
                    persisted_data[key] = pickle.load(file)
            results.append(context)

            shutil.rmtree(directory_name)
            os.remove(file_name)
        return results
